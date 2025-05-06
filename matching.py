from django.db.models import Q
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from django.contrib.auth import get_user_model
import logging

# Import models using the correct app label
from matrimonyapp.models import Profile, EducationProfessional

# Set up logging
logger = logging.getLogger(__name__)

class Matcher:
    def __init__(self, k=5):
        self.k = k
        self.preprocessor = None
        self.model = None
        self.feature_names = []
        
    def get_features(self, user):
        """Extract only the essential features for matching"""
        try:
            profile = Profile.objects.get(user=user)
            education = EducationProfessional.objects.get(user=user)
            
            features = {
                'denomination': profile.denomination,
                'marital_status': profile.marital_status,
                'education_level': education.education_level,
            }
            return features
        except Profile.DoesNotExist:
            logger.warning(f"Profile does not exist for user {user}")
            return None
        except EducationProfessional.DoesNotExist:
            logger.warning(f"EducationProfessional does not exist for user {user}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting features for user {user}: {e}")
            return None
    
    def preprocess_data(self, users):
        """Preprocess only the key matching criteria"""
        data = []
        valid_users = []
        
        for user in users:
            features = self.get_features(user)
            if features is not None:  # Only include users with complete data
                data.append(features)
                valid_users.append(user)
        
        if not data:
            return None, []
            
        df = pd.DataFrame(data)
        
        # OneHotEncode the categorical features
        self.preprocessor = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        processed_data = self.preprocessor.fit_transform(df)
        
        # Store feature names for debugging
        self.feature_names = self.preprocessor.get_feature_names_out()
        
        return processed_data, valid_users
    
    def fit(self, users):
        """Fit the KNN model with user data"""
        if not users:
            self.model = None
            return
            
        processed_data, valid_users = self.preprocess_data(users)
        
        if processed_data is None or not valid_users:
            self.model = None
            return
            
        # Calculate the actual number of neighbors we can request
        n_samples = len(valid_users)
        actual_k = min(self.k + 1, n_samples)  # +1 to account for self, but don't exceed sample size
        
        # Use Jaccard similarity instead of Hamming for better sparse compatibility
        self.model = NearestNeighbors(
            n_neighbors=actual_k,  # Use the adjusted k value
            metric='jaccard',      # Jaccard works well for binary categorical data
            algorithm='brute'      # Brute force works best for our small dataset
        )
        self.model.fit(processed_data)
        
    def get_matches(self, user, all_users):
        """Get matches where all three criteria match"""
        if not all_users:
            return []
            
        if not self.model:
            self.fit(all_users)
            if not self.model:  # Still no model after fit (empty data)
                return []
        
        # Get the target user's features
        user_features = self.get_features(user)
        if user_features is None:
            logger.warning(f"Cannot get matches for user {user} due to missing profile data")
            return []
            
        user_df = pd.DataFrame([user_features])
        try:
            user_processed = self.preprocessor.transform(user_df)
        except Exception as e:
            logger.error(f"Error transforming user features: {e}")
            return []
        
        # Find nearest neighbors (using Jaccard similarity)
        try:
            distances, indices = self.model.kneighbors(user_processed)
        except Exception as e:
            logger.error(f"Error finding neighbors: {e}")
            return []
        
        # Convert numpy indices to Python integers
        indices = indices[0].tolist()  # Convert to list of Python integers
        distances = distances[0].tolist()
        
        # Get matched users
        matches = []
        for i, distance in zip(indices, distances):
            try:
                # Ensure index is Python integer
                i = int(i)
                if i >= len(all_users):
                    logger.warning(f"Index {i} out of bounds for users list")
                    continue
                    
                match_user = all_users[i]
                if match_user.id == user.id:  # Skip self
                    continue
                    
                try:
                    profile = Profile.objects.get(user=match_user)
                    education = EducationProfessional.objects.get(user=match_user)
                    
                    # Check if all three criteria match
                    denomination_match = profile.denomination == user_features['denomination']
                    marital_match = profile.marital_status == user_features['marital_status']
                    education_match = education.education_level == user_features['education_level']
                    
                    # Only include if all three match
                    if denomination_match and marital_match and education_match:
                        matches.append({
                            'user': match_user,
                            'distance': distance,
                        })
                except (Profile.DoesNotExist, EducationProfessional.DoesNotExist) as e:
                    logger.warning(f"Match user {match_user} missing profile data: {e}")
                    continue
            except Exception as e:
                logger.error(f"Error processing match at index {i}: {e}")
                continue
        
        # Sort by distance (ascending)
        matches.sort(key=lambda x: x['distance'])
        return matches[:self.k]  # Return at most k matches