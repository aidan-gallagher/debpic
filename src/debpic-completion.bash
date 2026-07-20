# debpic bash completion


# This script is functionally correct but it is getting messy and
# I hope most of it could be converted to Python at some point.

_debpic_complete() {

  # Don't use colon as a special character
  # https://tiswww.case.edu/php/chet/bash/FAQ E13
  COMP_WORDBREAKS=${COMP_WORDBREAKS//:}

  local cur prev opts
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  opts="--help --no-cache --distribution --local-repository --sources --extra-pkg --destination --interactive --hook --vscode --delete-images -- "


  instances_of_double_dash=0
  # Change opts depending on existing words
  for word in "${COMP_WORDS[@]}"; do

# -------------------- Handle dpkg-buildpackage/(--) args -------------------- #
    if [[ "$word" == "--" ]]; then
      instances_of_double_dash+=1
    fi
    if [[ instances_of_double_dash -gt 1 ]]; then
      # Ideally we would supply dpkg-buildpackage tab completion here but that doesn't seem to exist :(
      return 0
    fi
    # If "--" is the current word then skip otherwise we wouldn't get any tab completion since all options start with --.
    if [[ "$word" == "--" && "--" != "$cur" ]]; then
      # Ideally we would supply dpkg-buildpackage tab completion here but that doesn't seem to exist :(
      return 0
    fi
# ---------------------------------------------------------------------------- #
    if [[ "$word" == "--delete-images" || "$word" == "-d" || "$word" == "--help" || "$word" == "-h" ]]; then
      return 0
    fi
    if [[ "$word" == "--no-cache" || "$word" == "-nc" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;s/--no-cache//')
    fi
    if [[ "$word" == "--distribution" || "$word" == "-d" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;s/--distribution//')
    fi
    if [[ "$word" == "--local-repository" || "$word" == "-lr" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;s/--local-repository//')
    fi
    if [[ "$word" == "--sources" || "$word" == "-s" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;s/--sources//')
    fi
    if [[ "$word" == "--extra-pkg" || "$word" == "-e" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;')
    fi
    if [[ "$word" == "--destination" || "$word" == "-dst" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;s/--destination//')
    fi
    if [[ "$word" == "--interactive" || "$word" == "-i" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;s/--interactive//;s/-- //;s/--vscode//')
    fi
    if [[ "$word" == "--hook" || "$word" == "-hk" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;s/--hook//')
    fi
    if [[ "$word" == "--vscode" || "$word" == "-vs" ]]; then
      opts=$(echo "$opts" | sed 's/--help//;s/--delete-images//;s/--vscode//;s/-- //;s/--interactive//;s/--no-cache//;s/--destination//;')
    fi
  done

  case "${prev}" in
    -d|--distribution)
      return 0
      ;;
    -lr|--local-repository)
      local directories=$(compgen -d -- "${cur}")
      COMPREPLY=( ${directories})
      return 0
    ;;
    -s|--sources)
      # Completing source file names without extensions in /etc/debpic/sources.list.d/
      local source_dir="/etc/debpic/sources.list.d/"
      local files=$(compgen -f -- "${source_dir}${cur}")
      if [ -n "${files}" ]; then
        COMPREPLY=( $(basename -a ${files} | sed 's/\..*//') )
      else
        COMPREPLY=()  # No matching files, so no completions
      fi
      return 0
      ;;
    -ep|--extra-pkg)
      # This is the same tab completion "apt install" uses.
      # It will be mostly correct but the host OS package list may be different to what the container OS package list is.
      COMPREPLY=( $( apt-cache --no-generate pkgnames "$cur" \
          2> /dev/null ) )
      return 0
      ;;
    -dst|--destination)
      return 0
      ;;
    -hk|--hook)
      # Completing source file names without extensions in /etc/debpic/sources.list.d/
      local source_dir="/etc/debpic/hooks/"
      local files=$(compgen -f -- "${source_dir}${cur}")
      if [ -n "${files}" ]; then
        COMPREPLY=( $(basename -a ${files}))
      else
        COMPREPLY=()  # No matching files, so no completions
      fi
      return 0
      ;;
    *)
      ;;
  esac

  COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
  return 0
}

complete -F _debpic_complete debpic
