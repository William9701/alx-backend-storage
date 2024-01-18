-- This sql querry Creates a stored procedure AddBonus
DELIMITER $$
CREATE PROCEDURE AddBonus(
    IN p_user_id INT,
    IN p_project_name VARCHAR(255),
    IN p_score INT
)
BEGIN
    DECLARE project_id INT;

    -- Check properly if the project already exists
    SELECT id INTO project_id FROM projects WHERE name = p_project_name;
    
    -- If the project does not exist then create it
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (p_project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Add the bonus correction
    INSERT INTO corrections (user_id, project_id, score) VALUES (p_user_id, project_id, p_score);
END;
$$
DELIMITER ;