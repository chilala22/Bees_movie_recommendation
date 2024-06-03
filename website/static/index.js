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

  // setTimeout(function() {
  //   var errorMessages = document.getElementById('error-messages');
  //   if (errorMessages) {
  //     errorMessages.parentNode.removeChild(errorMessages);
  //   }
  // }, 5000);
  setTimeout(function() {
    var errorMessages = document.getElementById('error-messages');
    if (errorMessages) {
      errorMessages.classList.add('hide');
      resetFormPosition();
        // Scroll the page back to the top
    scrollToTop();
    }
  }, 5000);

//   setTimeout(() => {
//     // Hide the error message
//     const errorMessage = document.getElementById('error-message');
//     errorMessage.style.display = 'none';

//     // Reset the form position
//     resetFormPosition();
// }, 3000);
function resetFormPosition() {
    const form = document.getElementById('my-form');
    form.style.transform = 'translateY(0)';
}
function scrollToTop() {
  window.scrollTo({
      top: 0,
      behavior: 'smooth'
  });
}

// function toggleModal(movieId) {
//   const modal = document.getElementById('rate-movie-modal');
//   modal.classList.toggle('hidden');
//   document.getElementById('movie_id').value = movieId;
// }
// function toggleModal(movieId) {
//   const modal = document.getElementById('rate-movie-modal');
//   modal.classList.toggle('hidden');
//   document.getElementById('movie_id').value = movieId;
//   console.log(document.getElementById('movie_form').action);
// }

// document.getElementById('rate_add').addEventListener('click', function(event) {
//   event.preventDefault();
//   toggleModal({{ movie_popular['id'] }});
// });

// const starRatings = document.querySelectorAll('.star-icon-wrapper');

// starRatings.forEach((starWrapper) => {
//   starWrapper.addEventListener('click', () => {
//     const rating = starWrapper.getAttribute('data-rating');
//     starRatings.forEach((wrapper) => {
//       wrapper.classList.remove('active');
//       if (parseInt(wrapper.getAttribute('data-rating')) <= rating) {
//         wrapper.classList.add('active');
//       }
//     });
//     document.getElementById(`ratings-${rating}`).checked = true;
//   });
// });

// const starRatings = document.querySelectorAll('.star-icon-wrapper');

// starRatings.forEach((starWrapper) => {
//   starWrapper.addEventListener('click', () => {
//     const rating = starWrapper.getAttribute('data-rating');
//     starRatings.forEach((wrapper) => {
//       wrapper.classList.remove('active');
//       if (parseInt(wrapper.getAttribute('data-rating')) <= rating) {
//         wrapper.classList.add('active');
//       }
//     });
//     document.getElementById(`ratings-${rating}`).checked = true;
//   });
// });

const starRatings = document.querySelectorAll('.star-icon-wrapper');
const ratingsInput = document.getElementById('ratings');

starRatings.forEach((starWrapper) => {
  starWrapper.addEventListener('click', () => {
    const rating = starWrapper.getAttribute('data-rating');
    ratingsInput.value = rating;
    starRatings.forEach((wrapper) => {
      wrapper.classList.remove('active');
      if (parseInt(wrapper.getAttribute('data-rating')) <= rating) {
        wrapper.classList.add('active');
      }
    });
  });
});

$(document).ready(function(){
  $('.recommendations-carousel').slick({
    slidesToShow: 5,
    slidesToScroll: 1,
    snapAlign: 'center',
    infinite: false,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
          snapAlign: 'center',
          infinite: false
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
          snapAlign: 'center',
          infinite: false
        }
      }
    ]
  });
});

