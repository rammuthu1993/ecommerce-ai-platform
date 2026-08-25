from app.audit.repository import save_audit_log, find_audit_logs

def log_audit(action, module, entity, entity_id=None, user_id=None, details=None, connection=None):
    return save_audit_log(
        action=action.upper(),
        module=module.upper(),
        entity=entity.upper(),
        entity_id=entity_id,
        user_id=user_id,
        details=details,
        connection=connection
    )

def get_audit_trail(page=1, limit=10, module=None, entity=None):
    return find_audit_logs(page=page, limit=limit, module=module, entity=entity)
