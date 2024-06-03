// function deleteNote(noteId){
//     // enpoint
//     fetch("/delete-note",{
//         method:"POST",
//         // turns into a string 
//         body:JSON.stringify({noteId:noteId})
//     }).then((_res)=>{
//         // how to reload the window
//         window.location.href ="/";
//     });
// }

function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

