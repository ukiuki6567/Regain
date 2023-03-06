# SQLのテンプレートを格納する部分

class SQLTemplates():
    PROCESS_UPDATE_SQL = """
    UPDATE
        processes
    SET
        process_name = '{process_name}'
    WHERE
        process_id = {process_id}
    """

    TASK_UPDATE_SQL = """
    UPDATE
        tasks
    SET
        task_name = '{task_name}',
        priority_id = {priority_id},
        deadline = '{deadline}'
    WHERE
        task_id = {task_id}    
    """