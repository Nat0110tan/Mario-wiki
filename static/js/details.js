var quill;
var toolbarOptions = [
  ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
  ['blockquote', 'code-block'],

  [{ 'header': 1 }, { 'header': 2 }],               // custom button values
  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
  [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
  [{ 'direction': 'rtl' }],                         // text direction

  [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
  [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
  ['image'],          // add's image support
  [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
  [{ 'font': [] }],
  [{ 'align': [] }],

  ['clean']                                         // remove formatting button
];
window.addEventListener("load", function() {

  
  quill = new Quill('#editor-post', {
      theme: 'snow',
      placeholder: 'Please enter your comment...',
      modules:{
        toolbar: toolbarOptions,
      }
  });

  const comment_form = document.getElementById('comment-form');
  comment_form.onsubmit = submit_entry;
  
});

function submit_entry() {
  const hidden_input = document.getElementById('postData');
  hidden_input.value = quill.root.innerHTML;
}