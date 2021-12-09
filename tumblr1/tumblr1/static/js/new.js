$(document).ready(function() 
{

        $("#post_type").change(function() {
            var name=$(this).val();
           
            if(name=='IMAGE')
            {
                $('#img_gif_video_msg').text('Please Select Image');
            }
            if(name=='VIDEO')
            {
                $('#img_gif_video_msg').text('choose Video');    
            }
            if(name=='GIF')
            {
                $('#img_gif_video_msg').text('Please Select GIF');    
            }
        });
        
});//document end

// $(".like_show").css('display','none')
// $("#unlike_hide").css('display','block')
function heartid(post_id) 
{
    var post_id=post_id;
    var like_post=true;
    console.log(post_id,like_post);
    $.ajax({
        type:"POST",
        url:"/like", 
        data:{"post_id":post_id,"like_post":like_post},
        datatype:"json",
        success: function(response)
        {
            if(response.status=="unlike")
            {
                var counttt=$("#like_count"+post_id).text();
                console.log(counttt);
                $("#unlike_hide"+post_id).css('display','none');
                $("#like_show"+post_id).css('display','block');
            }
            if(response.status=="like")
            {
                var counttt=$("#like_count"+post_id).text();
                console.log(counttt);
                $("#like_show"+post_id).css('display','none');
                $("#unlike_hide"+post_id).css('display','block');
            }
            if(response.status=="success")
            {
                var counttt=$("#like_count"+post_id).text();
                console.log(counttt);
                $("#unlike_hide"+post_id).css('display','none');
                $("#like_show"+post_id).css('display','block');
            }
            if(response.status=="unauthorized_user")
            {
                $.notify("Please Login","info");
            }   
        }
    });
}


