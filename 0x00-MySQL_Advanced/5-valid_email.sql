-- this is a triger that changes the valid email status to 0
DELIMITER $$
CREATE TRIGGER reset_valid_email
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
   IF OLD.email != NEW.email THEN
      UPDATE users
      SET valid_email = 0
      WHERE id = NEW.id;
   END IF;
END; $$
DELIMITER ;
