QUERY_HINT_PART = """
SELECT hint_part FROM users
WHERE telegram_id = {telegram_id};
"""

QUERY_HINT_ID = """
SELECT hint_id FROM users
WHERE telegram_id = {telegram_id};
"""

QUERY_HINT_DESCRIPTION = """
SELECT description_{hint_part} FROM hints
WHERE id = {hint_id};
"""

QUERY_UNSOLVED_HINT_ID = """
SELECT id FROM hints
WHERE claimed = 0;
"""

QUERY_UNSOLVED_TOKEN_ID = """
SELECT token_id FROM hints
WHERE claimed = 0;
"""

QUERY_ALL_HINTS = """
SELECT token_id FROM hints;
"""

QUERY_CURRENT_USERS = """
SELECT telegram_id FROM users
"""

QUERY_CURRENT_USERS_STUDENT_ID = """
SELECT student_id FROM users
"""

QUERY_UNCLAIMED_USERS = """
SELECT telegram_id FROM users
WHERE claimed = 0;
"""

QUERY_LAST_HINT_TIME = """
SELECT UNIX_TIMESTAMP(last_hint_time) FROM users 
WHERE telegram_id = {telegram_id};
"""

UPDATE_LAST_HINT_TIME = """
UPDATE users
SET last_hint_time = FROM_UNIXTIME({last_hint_time})
WHERE telegram_id = {telegram_id};
"""

SET_HINT_CLAIMED = """
UPDATE hints
SET claimed = 1
WHERE token_id = '{token_id}';
"""

SET_USER_CLAIMED = """
UPDATE users
SET claimed = 1
WHERE telegram_id = {telegram_id};
"""

ASSIGN_HINT_ID = """
UPDATE users
SET hint_id = {hint_id}
WHERE telegram_id = {telegram_id};
"""

SET_HINT_PART = """
UPDATE users
SET hint_part = {hint_part}
WHERE telegram_id = {telegram_id};
"""

INSERT_NEW_USER = """
INSERT INTO users(telegram_id)
VALUES ({telegram_id})
"""

UPDATE_STUDENT_ID = """
UPDATE users
SET student_id = {student_id}
WHERE telegram_id = {telegram_id}
"""