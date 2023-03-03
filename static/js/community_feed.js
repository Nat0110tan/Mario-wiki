var quill;

var toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
    ['blockquote', 'code-block'],

    [{ 'header': [2, 3, 4, false] }],                 // custom button values
    [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
    [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
    [{ 'direction': 'rtl' }],                         // text direction

    [ 'link', 'image', 'video'],          // add's image support
    [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
    [{ 'font': [] }],
    [{ 'align': [] }],

    ['clean']                                         // remove formatting button
];

window.addEventListener('DOMContentLoaded', function () {
    function showInput() {
       let dicussionForm = document.getElementById("postDicussionDiv");
       let toolBar = document.getElementsByClassName('ql-toolbar', 'ql-snow');
       if (dicussionForm.style.display == "block"){
        dicussionForm.style.display = "none";
        toolBar[0].parentNode.removeChild(toolBar[0]);
        } else {
            dicussionForm.style.display = "block";
            quill = new Quill('#editor', {
                modules: {
                    toolbar: toolbarOptions
                    },
                    placeholder: 'Compose a post...',
                    theme: 'snow'  // or 'bubble'
                });
        }
    }

    function cancel(){
        let toolBar = document.getElementsByClassName('ql-toolbar', 'ql-snow');
        let dicussionForm = document.getElementById("postDicussionDiv");
        toolBar[0].parentNode.removeChild(toolBar[0]);
        dicussionForm.style.display = "none";
    }

    function showHideFilter() {
        let options = document.getElementById("filterOptions");
        
        if (options.style.display === "block") {
          options.style.display = "none";
        } else {
          options.style.display = "block";
        }
      }

    function submit_discussion() {
        const hidden_input = document.getElementById('discussionData');
        hidden_input.value = quill.root.innerHTML;
        console.log(hidden_input.value)
    }

    let postButton = document.getElementById("create-discussion");
    postButton.onclick = showInput;

    
    let cancelPost = document.getElementById("cancel-post");
    cancelPost.onclick = cancel;
    

    let advancedFilter = document.getElementById("advancedFilter");
    advancedFilter.onclick = showHideFilter;

    const discussionForm = document.getElementById('discussionForm');
    discussionForm.onsubmit = submit_discussion;
})

const LOADING = "/static/images/noun-loading-5531341.png"
const ERROR = "/static/images/noun-error-1073622.png"

async function load (){
    //get all like button divs
    like_buttons = document.getElementsByClassName("button_like")
    console.log(like_buttons)
    for (let i = 0; i < like_buttons.length; i++) {
        let like_div = like_buttons[i]; 
        let id = like_div.getAttribute("data-id")
        
        // create an image for status update.
        let image = document.createElement("img")
        image.src = LOADING
        like_div.append(image)

        try {    
            // get the like count.
            let result = await fetch('/post/'+id+'/like')
            if(!result.ok) throw new Error("not ok");
            result = await result.json()
            let likes = result.likes
            let you_like = result.you_like

            // function for updating display.
            function update() {
                like_div.textContent = likes
                let likeButton = document.getElementById("like_button_" + id)
                if(you_like) {
                    likeButton.classList.add('fa-solid')
                    likeButton.style['color'] = 'red';
                } else {
                    likeButton.classList.remove('fa-solid')
                    likeButton.style['color'] = '';
                }
            }
            update();

            // on click
            let likeButton = document.getElementById("like_button_" + id)
            likeButton.addEventListener("click", async () => {

                // like or unlike
                try {
                    let method = "POST"
                    if (you_like) {
                        method = "DELETE"
                    }
                    // set the spinner
                    like_div.textContent=""
                    like_div.append(image);
                    // send the reqest
                    let result = await fetch('/post/'+id+'/like1', {method})
                    if(!result.ok) throw new Error("not ok");
                    // process results
                    result = await result.json()
                    likes = result.likes
                    you_like = result.you_like
                    update()
                } catch (error) {
                    console.log(error)
                    like_div.textContent="";
                    image.src = ERROR
                    like_div.append(image);
                }
            })
        } catch (error) {
            console.log(error)
            like_div.textContent="";
            image.src = ERROR
            like_div.append(image);
        }
    }
}
load();