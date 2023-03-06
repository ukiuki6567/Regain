# SQLのテンプレートを格納する部分

class SQLTemplates():
    ### /hoge配下で実行するSQL ###
    PROJECT_UPDATE_SQL = """
    UPDATE
        projects
    SET
        project_name = '{project_name}'
    WHERE
        project_id = {project_id}
    """

    PROJECT_DELETE_SQL = """
    DELETE FROM
        projects
    WHERE
        project_id = {project_id}
    """

    ### /project_id/hoge配下で実行するSQL ###
    PROCESS_UPDATE_SQL = """
    UPDATE
        processes
    SET
        process_name = '{process_name}'
    WHERE
        process_id = {process_id}
    """

    PROCESS_DELETE_SQL = """
    DELETE FROM
        processes
    WHERE
        process_id = {process_id}
    """

    ### /project_id/process_id/hoge配下で実行するSQL ###
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

    TASK_DELETE_SQL = """
    DELETE FROM
        tasks
    WHERE
        task_id = {task_id}
    """