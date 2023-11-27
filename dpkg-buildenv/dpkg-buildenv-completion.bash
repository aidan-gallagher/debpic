# dpkg-buildenv bash completion

_dpkg-buildenv_complete() {

  # Don't use colon as a special character
  # https://tiswww.case.edu/php/chet/bash/FAQ E13
  COMP_WORDBREAKS=${COMP_WORDBREAKS//:}

  local cur prev opts
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  opts="--help --no-cache --sources --interactive-tty --delete-images"

  # Change opts depending on existing words
  for word in "${COMP_WORDS[@]}"; do
    if [[ "$word" == "--delete-images" || "$word" == "-d" || "$word" == "--help" || "$word" == "-h" ]]; then
      return 0
    fi
    if [[ "$word" == "--sources" || "$word" == "-s" ]]; then
      opts="--no-cache --interactive-tty"
      break
    fi
    if [[ "$word" == "--no-cache" || "$word" == "-nc" ]]; then
      opts="--interactive-tty --sources"
      break
    fi
    if [[ "$word" == "--interactive-tty" || "$word" == "-it" ]]; then
      opts="--no-cache --sources"
      break
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
    *)
      ;;
  esac

  COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
  return 0
}

complete -F _dpkg-buildenv_complete dpkg-buildenv
