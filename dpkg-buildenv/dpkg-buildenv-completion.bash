# dpkg-buildenv bash completion

_dpkg-buildenv_complete() {

  # Don't use colon as a special character
  # https://tiswww.case.edu/php/chet/bash/FAQ E13
  COMP_WORDBREAKS=${COMP_WORDBREAKS//:}

  local cur prev opts
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  opts="--help --no-cache --sources --distribution --interactive --delete-images"

  # Change opts depending on existing words
  for word in "${COMP_WORDS[@]}"; do
    if [[ "$word" == "--delete-images" || "$word" == "-d" || "$word" == "--help" || "$word" == "-h" ]]; then
      return 0
    fi
    if [[ "$word" == "--sources" || "$word" == "-s" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;s/--sources//')
    fi
    if [[ "$word" == "--distribution" || "$word" == "-d" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;s/--distribution//')
    fi
    if [[ "$word" == "--no-cache" || "$word" == "-nc" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;s/--no-cache//')
    fi
    if [[ "$word" == "--interactive" || "$word" == "-i" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;s/--interactive//')
    fi
  done

  case "${prev}" in
    -s|--sources)
      # Completing source file names without extensions in /etc/dpkg-buildenv/sources.list.d/
      local source_dir="/etc/dpkg-buildenv/sources.list.d/"
      local files=$(compgen -f -- "${source_dir}${cur}")
      COMPREPLY=( $(basename -a ${files} | sed 's/\..*//') )
      return 0
      ;;
    -d|--distribution)
      return 0
      ;;
    *)
      ;;
  esac

  COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
  return 0
}

complete -F _dpkg-buildenv_complete dpkg-buildenv
