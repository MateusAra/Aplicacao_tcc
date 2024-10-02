class Profile:
    def __init__(self, media_grade, media_time, media_attempts) -> None:
        self.media_grade = media_grade
        self.media_time = media_time
        self.media_attempts = media_attempts

    def get_profile_critical():
        return Profile(media_grade=5149.598060229709, 
                       media_time=521.9846860643186, 
                       media_attempts=2.6094946401225116)
    
    def get_profile_regular():
        return Profile(media_grade=6327.875845238093, 
                       media_time=513.5779761904762, 
                       media_attempts=3.0785714285714287)
    
    def get_profile_good():
        return Profile(media_grade=6927.0773, 
                       media_time=510.5825, 
                       media_attempts=3.085)
