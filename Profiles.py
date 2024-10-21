class Profile:
    def __init__(self, media_grade, media_time, media_attempts) -> None:
        self.media_grade = media_grade
        self.media_time = media_time
        self.media_attempts = media_attempts

    def get_profile_critical():
        return Profile(media_grade=4581.484705882353, 
                       media_time=628.7450980392157, 
                       media_attempts=1.2352941176470589)
    
    def get_profile_regular():
        return Profile(media_grade=5330.5482339523, 
                       media_time=526.0477001703578, 
                       media_attempts=2.7325383304940374)
    
    def get_profile_good():
        return Profile(media_grade=6484.077394366193, 
                       media_time=514.5962441314554, 
                       media_attempts=3.1004694835680753)
