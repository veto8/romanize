#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEXICONS="$DIR/lexicons"
DUMPS="$DIR/dumps"
BASE_URL="https://kaikki.org/dictionary"
DUMP_THAI="kaikki.org-dictionary-Thai.jsonl"
DEFAULT_TEXT="สวัสดี"
COMMON="English:en French:fr German:de Japanese:ja Chinese:zh Korean:ko Spanish:es Russian:ru Portuguese:pt Italian:it"

echo -e "I'm ask.sh. What would you like to do? Enter a Task ID from the list below: \n"
echo -e "TaskID\t Description"
echo -e "1\t Install - poetry install"
echo -e "2\t Run - romanize a text (language + text)"
echo -e "3\t Build Thai lexicon - word->IPA from the Thai kaikki dump"
echo -e "4\t Test - py_compile + run the default sample"
echo -e "5\t Enter venv shell"
echo -e "6\t Add language - pick from the kaikki language list, download + build its lexicon"
echo -e "7\t Add common languages - download + build a fixed list of languages"
echo -e "8\t Update Thai dump - re-download the kaikki Thai dump"
echo -e "9\t Run examples"
echo -e "10\t Status - venv, dumps, lexicons"
echo -e "11\t Clean bytecode - remove __pycache__ and *.pyc"
echo -e "12\t Remove lexicons + dumps (destructive - re-add to rebuild)"
echo -e "0\t Exit"

until [ "$task" = "0" ]; do
read task

if [ "$task" = "1" ]; then
    echo "... ${task} -- Install"
    poetry install

elif [ "$task" = "2" ]; then
    echo "... ${task} -- Run"
    read -p "language code (default: th): " lang
    lang=${lang:-th}
    read -p "text (default: ${DEFAULT_TEXT}): " text
    text=${text:-${DEFAULT_TEXT}}
    poetry run romanize --lang "$lang" "$text"

elif [ "$task" = "3" ]; then
    echo "... ${task} -- Build Thai lexicon"
    mkdir -p "$LEXICONS"
    poetry run romanize-lexicon "$DUMPS/$DUMP_THAI" -o "$LEXICONS/th.tsv"

elif [ "$task" = "4" ]; then
    echo "... ${task} -- Test"
    python3 -m py_compile "$DIR/romanize/cli.py" "$DIR/romanize/lexicon.py" && echo "py_compile OK"
    poetry run romanize "${DEFAULT_TEXT}"

elif [ "$task" = "5" ]; then
    echo "... ${task} -- venv shell"
    poetry shell

elif [ "$task" = "6" ]; then
    echo "... ${task} -- Add language (pick from the kaikki list)"
    TMP=$(mktemp)
    curl -sS "$BASE_URL/" | grep -oE '<a href="[^/"]*/index\.html">[^<]+' \
        | sed -E 's#<a href="([^/"]*)/index\.html">(.*)#\1|\2#' \
        | grep -vE '^\.' > "$TMP"
    sed -i '/^All%20languages%20combined|/d' "$TMP"
    i=0
    while IFS='|' read -r enc display; do
        i=$((i + 1))
        printf "%3d  %s\n" "$i" "$display"
    done < "$TMP"
    read -p "pick a number or type part of the language name: " pick
    case "$pick" in
        ''|*[!0-9]*) line=$(grep -iF "|$pick" "$TMP" | head -1) ;;
        *) exact=$(wc -l < "$TMP"); [ "$pick" -le "$exact" ] && line=$(sed -n "${pick}p" "$TMP") ;;
    esac
    if [ -z "${line:-}" ]; then
        echo "no match - rerun task 6 to browse the list"
    else
        enc=${line%%|*}
        f=${enc//%20/}
        read -p "language code for lexicons/<code>.tsv (e.g. fr): " lcode
        if [ -n "$lcode" ]; then
            mkdir -p "$LEXICONS" "$DUMPS"
            if curl -sSLo "$DUMPS/kaikki.org-dictionary-${f}.jsonl" "${BASE_URL}/${enc}/kaikki.org-dictionary-${f}.jsonl"; then
                poetry run romanize-lexicon "$DUMPS/kaikki.org-dictionary-${f}.jsonl" -o "$LEXICONS/${lcode}.tsv" || echo "lexicon build failed"
            else
                echo "download failed - rerun task 6"
                rm -f "$DUMPS/kaikki.org-dictionary-${f}.jsonl"
            fi
        else
            echo "language code required"
        fi
    fi
    rm -f "$TMP"

elif [ "$task" = "7" ]; then
    echo "... ${task} -- Add common languages"
    mkdir -p "$LEXICONS" "$DUMPS"
    for pair in ${COMMON}; do
        lname=${pair%%:*}
        lcode=${pair##*:}
        f=${lname//%20/}
        echo "--- ${lname} (${lcode}) ---"
        curl -sSLo "$DUMPS/kaikki.org-dictionary-${f}.jsonl" "${BASE_URL}/${lname}/kaikki.org-dictionary-${f}.jsonl" || { echo "skipped ${lname}"; continue; }
        poetry run romanize-lexicon "$DUMPS/kaikki.org-dictionary-${f}.jsonl" -o "$LEXICONS/${lcode}.tsv" || echo "lexicon build failed"
    done

elif [ "$task" = "8" ]; then
    echo "... ${task} -- Update Thai dump"
    mkdir -p "$DUMPS"
    curl -sSLo "$DUMPS/$DUMP_THAI" "${BASE_URL}/Thai/${DUMP_THAI}"

elif [ "$task" = "9" ]; then
    echo "... ${task} -- Examples"
    poetry run romanize "สวัสดี"
    poetry run romanize "สวัสดีครับ"
    poetry run romanize "ขอบคุณ"

elif [ "$task" = "10" ]; then
    echo "... ${task} -- Status"
    poetry env info --path
    ls -lh "$DUMPS/" 2>/dev/null || echo "no dumps"
    ls -lh "$LEXICONS/" 2>/dev/null || echo "no lexicons"

elif [ "$task" = "11" ]; then
    echo "... ${task} -- Clean bytecode"
    find "$DIR" -type d -name __pycache__ -exec rm -rf {} +
    find "$DIR" -type f -name "*.pyc" -delete
    echo "cleaned"

elif [ "$task" = "12" ]; then
    echo "... ${task} -- Remove lexicons + dumps"
    rm -rf "$LEXICONS"
    rm -rf "$DUMPS"
    echo "removed $LEXICONS and $DUMPS (rerun 8 + 3 or 6/7 to rebuild)"

else
    echo "Goodbye! - Exit"
    break
fi

sleep 3
exec ./ask.sh

done