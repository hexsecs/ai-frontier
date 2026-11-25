# Trusted main only. Update an existing check instead of appending statuses.
set_check() {
  local sha="$1" status="$2" conclusion="${3:-}" ids id
  [[ "$sha" =~ ^[0-9a-f]{40}$ ]] || return 1
  ids=$(gh api --paginate --slurp "repos/$GITHUB_REPOSITORY/commits/$sha/check-runs?check_name=review-policy&filter=all&per_page=100" | jq -ce '[.[].check_runs[] | select(.name=="review-policy" and .app.slug=="github-actions" and .external_id=="ai-frontier-review-policy-v1") | .id]')
  local -a fields=(-f name=review-policy -f status="$status" -f external_id=ai-frontier-review-policy-v1)
  if [[ "$status" == completed ]]; then
    fields+=(-f conclusion="$conclusion" -f completed_at="$(date -u +%FT%TZ)")
  fi
  if [[ "$(jq length <<<"$ids")" == 0 ]]; then
    gh api --method POST "repos/$GITHUB_REPOSITORY/check-runs" -f head_sha="$sha" "${fields[@]}" >/dev/null
  else
    # Update all matching runs if a prior interrupted creation left duplicates.
    for id in $(jq -r '.[]' <<<"$ids"); do
      gh api --method PATCH "repos/$GITHUB_REPOSITORY/check-runs/$id" "${fields[@]}" >/dev/null || return 1
    done
  fi
}
