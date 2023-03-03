var quill;
var toolbarOptions = [
  [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
  [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
  [{ 'font': [] }],

  ['bold', 'italic', 'underline'],        // toggled buttons
  ['blockquote', 'code-block'],

  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent

  ['clean']                                         // remove formatting button
];

window.addEventListener("load", function() {

    
    quill = new Quill('#editor-text', {
        theme: 'snow',
        placeholder: 'Please enter your bio...',
        modules:{
          toolbar: toolbarOptions,
        }
    });


    function update(){
        document.getElementById("update-form").style.display = "block";
        document.getElementById("upload-form").style.display = "block";
        document.getElementById("update-btn").style.display = "none";
    }

    let updatebtn = document.getElementById("update-btn");
    updatebtn.onclick = update;

    document.getElementById("decline-btn").addEventListener("click", function(event){
        event.preventDefault();
        document.getElementById("update-form").style.display = "none";
        document.getElementById("upload-form").style.display = "none";
        document.getElementById("update-btn").style.display = "block";
    });
    
    let form = document.getElementById('update-form');
    let newbio = document.getElementById('postData');

    form.onsubmit = function () {
        newbio.value = quill.root.innerHTML;
    }

    document.querySelector('#upload-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const response = await fetch('/profile/upload', {
          method: 'POST',
          body: formData,
        });
        if (response.ok) {
            this.alert("Successfully updated your profile photo!");
          // Handle successful upload
        } else {
          // Handle upload failure
          this.alert("Updated failed, please try again.");
        }
      });
    
});