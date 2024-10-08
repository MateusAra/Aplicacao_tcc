class Profile:
    def __init__(self, media_grade, media_time, media_attempts) -> None:
        self.media_grade = media_grade
        self.media_time = media_time
        self.media_attempts = media_attempts

    def get_profile_critical():
        return Profile(media_grade=4248.285818181818, 
                       media_time=583.0181818181818, 
                       media_attempts=1.2181818181818183)
    
    def get_profile_regular():
        return Profile(media_grade=5232.494671120401, 
                       media_time=516.371237458194, 
                       media_attempts=2.737458193979933)
    
    def get_profile_good():
        return Profile(media_grade=6549.906853818914, 
                       media_time=510.38442083965606, 
                       media_attempts=2.894284269094588)
