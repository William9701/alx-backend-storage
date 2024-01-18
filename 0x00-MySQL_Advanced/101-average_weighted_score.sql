-- Create stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Update users' average_score
    UPDATE users
    SET average_score = (
        SELECT IFNULL(SUM(corrections.score * projects.weight) / SUM(projects.weight), 0)
        FROM corrections
        LEFT JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = users.id
    );
END //

DELIMITER ;