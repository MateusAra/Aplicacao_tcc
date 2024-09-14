use moodle_tcc_1

select * from mdl_user
select * from mdl_quiz_sections
select * from mdl_quiz_slots
select * from mdl_grade_items where ItemName = 'TREINO NINJA [Tópico 01]'
select * from mdl_course_modules order by module
select * from mdl_course_modules_completion
select * from mdl_modules order by 1 desc
select * from mdl_quiz 
select  from_unixtime( timeopen, '%d/%m/%Y %h:%i:%s') as abriu,  from_unixtime( timeclose, '%d/%m/%Y %h:%i:%s') as fechou from mdl_quiz
select * from mdl_quiz_attempts where quiz = 4 and userId = 79 and attempt = 1
select
    a.id,
	q.name,
    q.attempts as attempts_permited,
    a.quiz,
    a.userid,
    a.attempt as attempts_realized,
    a.sumgrades as grade_attempt
/*from_unixtime( (timefinish - timestart), '%i:%s') as tempo*/
from 
	mdl_quiz as q
    inner join mdl_quiz_attempts as a on q.id = a.quiz
where a.quiz = 4 and a.userId = 79

SELECT
i.id, 
i.itemname,
i.itemtype,
i.itemmodule,
g.finalgrade,
i.courseid,
g.userid
FROM mdl_grade_items as i 
INNER JOIN mdl_grade_grades as g ON i.id=g.itemid
where i.id = 8


SELECT 
    i.id,
    i.itemname,
    i.itemtype,
    i.itemmodule,
    g.userid,
    g.finalgrade
FROM mdl_grade_items as i 
INNER JOIN mdl_grade_grades as g 
    ON i.id = g.itemid 
GROUP BY 
    i.id,
    i.itemname,
    i.itemtype,
    i.itemmodule,
    g.userid;
    
    
    
    SELECT distinct
		cm.id,m.name AS modulename,
        cm.idnumber,
        cm.added,
        cm.completion,
        cm.added AS timecreated,
        cm.section,
        s.name AS sectionname,
        i.itemname,
		i.itemtype,
		i.itemmodule
	FROM mdl_course_modules cm 
		INNER JOIN mdl_modules m ON m.id = cm.module  
        INNER JOIN mdl_course c ON c.id = cm.course 
        INNER JOIN mdl_course_sections s ON s.id = cm.section
        INNER JOIN mdl_grade_items as i on c.id = i.courseid
		INNER JOIN mdl_grade_grades as g ON i.id = g.itemid 
	where 
		cm.Section = 1
