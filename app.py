username, ts
        FROM slack.messages
        WHERE channel_id = '{SLACK_CHANNEL}'
        ORDER BY ts DESC LIMIT 10
    """
    slack, err = run_coral(slack_q)
    if err: errors.append(f"Slack: {err}"); slack = []

    duplicates = find_duplicates(issues or [])
    release_notes = draft_release_notes(prs)

    return jsonify({
        'issues': issues or [],
        'prs': prs or [],
        'cross_join': cross_join or [],
        'slack': slack or [],
        'duplicates': duplicates,
        'release_notes': release_notes,
        'status': 'ok',
        'warnings': errors
    })


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'github_user': GITHUB_USER, 'repo': GITHUB_REPO})


if name == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
