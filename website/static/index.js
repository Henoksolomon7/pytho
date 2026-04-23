function deleteNote(event, noteId) {
    event.preventDefault();

    fetch("/delete-note", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ noteId: noteId })
    }).then(() => {
        location.reload();
    });
}