select
	q.name,
    q.attempts as attempts_permited,
    a.quiz,
    a.attempt as attempts_realized,
    a.sumgrades as grade_attempt,
	from_unixtime( (a.timefinish - a.timestart), '%i:%s') as time_to_conclusion,
    u.username,
    a.userid,
    a.state
from 
	mdl_quiz as q
    inner join mdl_quiz_attempts as a on q.id = a.quiz
    inner join mdl_user as u on a.userid = u.id
where 
	a.quiz between 3 and 18
    order by quiz desc