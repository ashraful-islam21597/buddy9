const message = document.getElementById("message");
const notification = document.getElementById("notification")
const overlay = document.getElementById("overlay")
const btnPost = document.getElementById("btn-post")
const writePost = document.getElementById("write-post")
const meDropdown = document.getElementById("meDropdown")
const statusCard = document.querySelectorAll(".sc");
const privacyModal = document.getElementById('privacy-modal')
const commentPrivacyModal = document.getElementById('comment-privacy-modal')
let commentRoot, reply;

// close every modal if Overlay clicked
const openCloseOverlay = () =>{
  if (message.classList.contains('d-none') && notification.classList.contains('d-none') && meDropdown.classList.contains('d-none') && writePost.classList.contains('d-none') && privacyModal.classList.contains('d-none') && commentPrivacyModal.classList.contains('d-none')) {
    overlay.classList.add('d-none');
  } else {
    overlay.classList.remove('d-none');
  }
}
overlay.addEventListener("click", () => {
  message.classList.add('d-none')
  notification.classList.add('d-none')
  meDropdown.classList.add('d-none')
  overlay.classList.add('d-none');
  writePost.classList.add('d-none')
  privacyModal.classList.add('d-none')
  commentPrivacyModal.classList.add('d-none')
})

// Replying comment
for (let i = 0; i < statusCard.length; i++) {
  commentRoot = document.querySelectorAll(`.sc${i + 1}-comment-root`);
  for (let j = 0; j < commentRoot.length; j++) {
    let comment = document.getElementById(`sc${i + 1}-comment${j + 1}`)
    reply = document.querySelectorAll(`.sc${i + 1}-comment${j + 1}-reply`)
    for (let k = 0; k < reply.length; k++) {
      reply[k].addEventListener("click", () => {
        let replyArea = document.getElementById(`sc${i + 1}-smile1`);
        if (!replyArea) {
          let commentWriteAreaDiv = document.createElement('div');
          const commentWriteArea = `
          <div class="my-comment-area d-flex pt-2">
            <div class="my-dp mr-3">
              <img src="img/me.jpg" class="img-fluid" style="width: 38px; height: 38px; border-radius: 50%;"
                alt="">
            </div>
            {% for i in comments_set.all %}
            <div class="write-my-comment">
              <form action="" class="comment-input d-flex justify-content-between"  method="post">
                {% csrf_token %}
                <div>
                  <input type="text" placeholder="Write a comment">
                </div>
                <div class="media-comment">
                  <input type="file" id="sc${i + 1}-smile1" class="d-none ">
                  <label for="sc${i + 1}-smile1"><i class="far fa-smile mx-2"></i></label>
                  <input type="file" id="sc${i + 1}-image-comment1" class="d-none">
                  <label for="sc${i + 1}-image-comment1"><i class="far fa-image mx-2"></i></label>
                </div>
                <button type="submit">reply</button>
              </form>
            </div>
          </div>`;
          commentWriteAreaDiv.innerHTML = commentWriteArea;
          comment.appendChild(commentWriteAreaDiv);
        }
      })
    }
  }
}

// Disable scrolling when modals are open
document.querySelector('section').addEventListener('scroll', () => {
  window.scrollTo(0, 0);
})

// Navbar Notification,message and profile dropdown
document.getElementById("messageing").addEventListener("click", () => {
  openModal(message, notification, meDropdown)
})
document.getElementById("notifications").addEventListener("click", () => {
  openModal(notification, message, meDropdown)
})
document.getElementById("me").addEventListener("click", () => {
  openModal(meDropdown, notification, message)
})

function openModal(modal1, modal2, modal3) {
  modal2.classList.add('d-none')
  modal3.classList.add('d-none')
  modal1.classList.toggle('d-none');
  openCloseOverlay()
};

////////////////////////////////////// Write Post Modal ///////////////////////////////////
// close and open write post modal
const closePostModal = () => {
  writePost.classList.add('d-none')
  overlay.classList.add('d-none');
}
const openPostModal = () => {
  writePost.classList.remove('d-none')
  overlay.classList.remove('d-none');
}
document.getElementById("close-write-post").addEventListener("click",closePostModal)
document.getElementById('post-button').addEventListener("click",(e)=>{
  e.preventDefault()
  closePostModal()
})
document.getElementById("btn-post").addEventListener("click",openPostModal)

// Auto grow text area
const autoGrow = (element) => {
  element.style.height = '56px'
  element.style.height = (element.scrollHeight) + 'px'
}

/////////////////// Upload files //////////////////
let file;

// Upload File by button click
const input11 = document.getElementById('file11');
const input22 = document.getElementById('file22');
const input1 = document.getElementById('file1');
const input2 = document.getElementById('file2');
const button11 = document.getElementById('btn-file11');
const button22 = document.getElementById('btn-file22');
const button1 = document.getElementById('btn-file1');
const button2 = document.getElementById('btn-file2');
button11.onclick = (e) => {
  e.preventDefault()
  input11.click()
}
input11.addEventListener('change', function (e) {
  file = this.files[0]
  showFile()
})
button22.onclick = (e) => {
  e.preventDefault()
  input22.click()
}
input22.addEventListener('change', function (e) {
  file = this.files[0]
  showFile()
})
button1.onclick = (e) => {
  e.preventDefault()
  console.log('ok')
  openPostModal()
  input1.click()
}
input1.addEventListener('change', function (e) {
  file = this.files[0]
  showFile()
})
button2.onclick = (e) => {
  e.preventDefault()
  openPostModal()
  input2.click()
}
input2.addEventListener('change', function (e) {
  file = this.files[0]
  showFile()
})

// Drop and drag file
const dropArea = document.getElementById('dropArea');
const dragText = document.getElementById('dragText');
dropArea.addEventListener('dragover', (event) => {
  event.preventDefault();
  dragText.classList.remove('d-none')
})

dropArea.addEventListener('dragleave', (event) => {
  event.preventDefault();
  dragText.classList.add('d-none')
})

dropArea.addEventListener('drop', (event) => {
  event.preventDefault();
  dragText.classList.add('d-none')
  file = event.dataTransfer.files[0]
  showFile()
})

//////////// show uploaded files ////////////
const showFile = () => {
  let fileType = file.type;
  let validImageExtensions = ['image/png', 'image/jpg', 'image/jpeg']
  let validVideoExtensions = ['video/mp4', 'video/mpeg-4']
  if (validImageExtensions.includes(fileType)) {
    let fileReader = new FileReader()
    fileReader.onload = () => {
      let fileURL = fileReader.result
      let imgDiv = `
      <div class = "img">
        <img src = "${fileURL}" width="540px"/>
        <button id="close1" class="closeImg">&times;</button>
      </div> `
      dropArea.innerHTML = imgDiv
      closeImgFun('close1')
    }
    fileReader.readAsDataURL(file)
  } else if (validVideoExtensions.includes(fileType)) {
    let fileReader = new FileReader()
    fileReader.onload = () => {
      let fileURL = fileReader.result
      let imgDiv = `
      <div class = "video">
        <video width="540px" controls>
          <source src="${fileURL}">
        </video>
        <button id="close2" class="closeImg">&times;</button>
      </div> `
      dropArea.innerHTML = imgDiv
      closeImgFun('close2')
    }
    fileReader.readAsDataURL(file)
  } else {
    alert('Not Valid File Format')
  }
}

// close after reviewing the posts video or photo
const closeImgFun = (close) => {
  document.getElementById(close).addEventListener('click', () => {
    dropArea.innerHTML = ''
  })
}

////////////////////// Privacy Modal /////////////////////////
const closePrivacy = () => {
  privacyModal.classList.add('d-none')
  writePost.classList.remove('d-none')
}
document.getElementById('privacy-open-button').addEventListener('click', () => {
  privacyModal.classList.remove('d-none')
  writePost.classList.add('d-none')
})
document.getElementById('close-privacy').addEventListener('click', closePrivacy)
document.getElementById('privacy-cancel-button').addEventListener('click', closePrivacy)
document.getElementById('privacy-save-button').addEventListener('click', closePrivacy)

///////////////////// Comment Privacy Modal //////////////////
const closeCommentPrivacy = () => {
  commentPrivacyModal.classList.add('d-none')
  writePost.classList.remove('d-none')
}

document.getElementById('comment-privacy-open-button').addEventListener('click', (e) => {
  e.preventDefault()
  commentPrivacyModal.classList.remove('d-none')
  writePost.classList.add('d-none')
})
document.getElementById('close-comment-privacy').addEventListener('click', closeCommentPrivacy)
document.getElementById('comment-privacy-cancel-button').addEventListener('click', closeCommentPrivacy)
document.getElementById('comment-privacy-save-button').addEventListener('click', closeCommentPrivacy)

//////////////////////// New DP Modal ///////////////////////
// document.getElementById('new-dp1')

//////////////////// Status Photo Modal /////////////////////
