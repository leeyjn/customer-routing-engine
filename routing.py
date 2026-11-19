"""Pure, synthetic routing rules. No calendars, CRM or outbound messages."""
def assign(request, team, loads, recent_owner=None, designated_owner=None,
           open_owner=None, declined=()):
    if request.get('do_not_contact'):
        return {'owner': None, 'action': 'suppress', 'reason': 'contact_not_allowed'}
    eligible = sorted(set(team) - set(declined))
    if not eligible:
        return {'owner': None, 'action': 'manual_review', 'reason': 'no_eligible_owner'}
    if open_owner in eligible:
        return {'owner': open_owner, 'action': 'merge', 'reason': 'existing_open_request'}
    for owner, reason in [(request.get('explicit_owner'), 'explicit_instruction'),
                          (recent_owner, 'recent_customer_context'),
                          (designated_owner, 'designated_owner')]:
        if owner in eligible:
            return {'owner': owner, 'action': 'assign', 'reason': reason}
    owner = min(eligible, key=lambda person: (loads.get(person, 0), person))
    return {'owner': owner, 'action': 'assign', 'reason': 'lowest_current_load'}


if __name__ == '__main__':
    import json
    team = ['DEMO-AGENT-A', 'DEMO-AGENT-B']
    loads = {'DEMO-AGENT-A': 4, 'DEMO-AGENT-B': 1}
    print(json.dumps({'synthetic': True, 'decision': assign({}, team, loads,
          recent_owner='DEMO-AGENT-A')}, indent=2))
