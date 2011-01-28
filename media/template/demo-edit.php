<?php include "./inc/template.php"; 
head(
  $title = 'Editing Demo: The Incredible Machine | Mozilla Developer Network',
  $pageid = '', 
  $bodyclass = 'section-demos',
  $headerclass = 'compact'
); ?>
<section id="nav-toolbar">
<div class="wrap">
  <nav class="crumbs">
    <ol role="navigation">
      <li><a href="home.php">MDN</a></li>
      <li><a href="demos-landing.php">Demo Studio</a></li>
      <li><a href="demo-detail.php">The Incredible Machine</a></li>
      <li>Edit</li>
    </ol>
  </nav>
</div>
</section>

<section id="content">
<div class="wrap">

  <section id="content-main" role="main">
    <h1 class="page-title">Editing Demo: The Incredible Machine</h1>

    <form id="demo-submit" class="submission" enctype="multipart/form-data" method="post" action="path/to/handler">
      <fieldset class="section">
        <legend><b>Describe Your Demo</b></legend>
        <ul>
          <li>
            <label for="title">Demo Name</label>
            <input type="text" id="title" name="title" value="The Incredible Machine">
          </li>
          <li>
            <label for="summary">Summary description (no more than two lines)</label>
            <textarea id="summary" name="summary" rows="2" cols="60">Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat.</textarea>
          </li>
          <li>
            <label for="description">Detailed description <em class="note">(optional)</em></label>
            <textarea id="description" name="description" rows="8" cols="60">
Donec nec justo eget felis facilisis fermentum. Aliquam porttitor mauris sit amet orci. Aenean dignissim pellentesque felis.

Morbi in sem quis dui placerat ornare. Pellentesque odio nisi, euismod in, pharetra a, ultricies in, diam. Sed arcu. Cras consequat.

Praesent dapibus, neque id cursus faucibus, tortor neque egestas augue, eu vulputate magna eros eu erat. Aliquam erat volutpat. Nam dui mi, tincidunt quis, accumsan porttitor, facilisis luctus, metus.

Phasellus ultrices nulla quis nibh. Quisque a lectus. Donec consectetuer ligula vulputate sem tristique cursus. Nam nulla quam, gravida non, commodo a, sodales sit amet, nisi.

Pellentesque fermentum dolor. Aliquam quam lectus, facilisis auctor, ultrices ut, elementum vulputate, nunc.
            </textarea>
          </li>
          <li>
            <fieldset class="inline">
              <legend><b>Select up to five technologies used in your demo.</b></legend>
              <ul id="tech-tags" class="cols-4">
                <li><label class="disabled"><input type="checkbox" name="audio" disabled="disabled"> Audio</label></li>
                <li><label><input type="checkbox" name="canvas" checked="checked"> Canvas</label></li>
                <li><label><input type="checkbox" name="css3" checked="checked"> CSS3</label></li>
                <li><label class="disabled"><input type="checkbox" name="device" disabled="disabled"> Device</label></li>
                <li><label class="disabled"><input type="checkbox" name="files" disabled="disabled"> Files</label></li>
                <li><label class="disabled"><input type="checkbox" name="fonts" disabled="disabled"> Fonts</label></li>
                <li><label class="disabled"><input type="checkbox" name="forms" disabled="disabled"> Forms</label></li>
                <li><label class="disabled"><input type="checkbox" name="geolocation" disabled="disabled"> Geolocation</label></li>
                <li><label><input type="checkbox" name="javascript" checked="checked"> JavaScript</label></li>
                <li><label><input type="checkbox" name="html5" checked="checked"> HTML5</label></li>
                <li><label class="disabled"><input type="checkbox" name="indexeddb" disabled="disabled"> IndexedDB</label></li>
                <li><label class="disabled"><input type="checkbox" name="dragndrop" disabled="disabled"> Drag and Drop</label></li>
                <li><label class="disabled"><input type="checkbox" name="mobile" disabled="disabled"> Mobile</label></li>
                <li><label class="disabled"><input type="checkbox" name="multitouch" disabled="disabled"> Multi-touch</label></li>
                <li><label class="disabled"><input type="checkbox" name="offline" disabled="disabled"> Offline Storage</label></li>
                <li><label><input type="checkbox" name="svg" checked="checked"> SVG</label></li>
                <li><label class="disabled"><input type="checkbox" name="video" disabled="disabled"> Video</label></li>
                <li><label class="disabled"><input type="checkbox" name="webgl" disabled="disabled"> WebGL</label></li>
                <li><label class="disabled"><input type="checkbox" name="websockets" disabled="disabled"> WebSockets</label></li>
                <li><label class="disabled"><input type="checkbox" name="webworkers" disabled="disabled"> Web Workers</label></li>
                <li><label class="disabled"><input type="checkbox" name="xhr" disabled="disabled"> XMLHttpRequest</label></li>
              </ul>
            </fieldset>
          </li>
        </ul>
      </fieldset>

<script type="text/javascript">
// <![CDATA[
	$(document).ready(function(){
		$("#tech-tags input[type=checkbox]").click(function(){
		  var count = $("#tech-tags input[type=checkbox]:checked").length >= 5;
		  $("#tech-tags input[type=checkbox]").not(":checked").attr("disabled",count);

		  $("#tech-tags input[type=checkbox]").each(function(){
		    if ($(this).is(":disabled")) {
		      $(this).parents("label").addClass("disabled");
		    }
		    else {
		      $(this).parents("label").removeClass("disabled");
		    }
		  });

		});
	});	
// ]]>
</script>

      <fieldset class="section">
        <legend><b>Show Off Your Demo</b></legend>
        
        <ul>
          <li>
            <label for="screenshot">Provide at least one screenshot of your demo.</label>
            <div class="fileslist">
              <ul class="sortable">
                <li>title-screen.jpg <button type="button" class="remove">Remove</button></li>
                <li>gameplay-screenshot-1.jpg <button type="button" class="remove">Remove</button></li>
                <li>game-over-screen.jpg <button type="button" class="remove">Remove</button></li>
              </ul>
              <p class="add"><input type="file" id="screenshot" name="screenshot_1" class="filebutton" title="Upload another screenshot&hellip;"></p>
              <p class="note">JPEG and PNG supported. Minimum size of 480&times;360.</p>
            </div>
          </li>
          <li>
            <label for="video">Provide a link to a video of your demo in action, for viewers who can’t or don’t want to run it. <em class="note">(optional)</em></label>
            <input type="text" id="video" name="video" value="http://www.youtube.com/watch?v=rYntjR4-pY4">
            <p class="note">We support YouTube, Vimeo, and DailyMotion.</p>
          </li>
        </ul>
      </fieldset>

      <div id="prepare-demo" class="module aside">
        <h3 class="mod-title">Preparing Your Demo</h3>
        <ul>
          <li>Your demo’s source code should be packaged inside a Zip file.</li>
          <li>The main page of your demo should be a file named <code>index.html</code> in the root of the Zip.</li>
          <li>Your demo should be build on client-side technology (HTML, CSS, Javascript). Server-side languages like PHP and Ruby are not supported.</li>
          <li>If your demo requires external resources, it should use AJAX to access them.</li>
          <li>To submit your demo, you need an <a href="/signup/">MDN account</a>.</li>
        </ul>
      </div>
      
      <fieldset class="section">
        <legend><b>Provide the Source Code</b></legend>
        <ul>
          <li>
            <b class="label">Source code Zip file</b>
            <input type="text" readonly="readonly" value="incred_machine_v01.zip">
          </li>
          <li>
            <label for="demo_package">Update source code</label>
            <input type="file" id="demo_package" name="demo_package" class="filebutton" title="Replace demo file&hellip;">
          </li>
          <li>
            <label for="source_code_url">Is your source code also available somewhere else on the web (e.g., github)? Please share the link.</label>
            <input type="text" id="source_code_url" name="source_code_url" value="https://github.com/myhandle/myproject">
          </li>
          <li>
            <label for="license">Select the license that applies to your source code.</label>
            <select id="license" name="license">
              <option value="apache">Apache</option>
              <option value="bsd">BSD</option>
              <option value="gpl" selected="selected">GPL</option>
              <option value="mpl">MPL</option>
            </select>
          </li>
        </ul>
      </fieldset>

<script type="text/javascript">
// <![CDATA[

  /* Add isChildOf method to determine if the element is a descendant of another specified element.
   * Usage: $(element).isChildOf(filter_string)
   */
  (function($) {
    $.fn.extend({
      isChildOf: function( filter_string ) {    
        var parents = $(this).parents().get(); 
        for ( j = 0; j < parents.length; j++ ) {
          if ( $(parents[j]).is(filter_string) ) {
            return true;
          }
        }  
        return false;
      }
    });
  })(jQuery);

	$("input.filebutton").each(function(){
    var text = $(this).attr("title");
    var file = $(this).val();

    if ( $(this).isChildOf(".fileslist") ) {
      $(this).closest("p").addClass("replaced").append('<div class="replacement"><span class="button">'+text+'</span></div>');
    }
    else {
		  $(this).closest("li, p").addClass("replaced").append('<div class="replacement"><span class="button">'+text+'</span><input class="filename" type="text" readonly="readonly" value="'+file+'"></div>');
      $(this).change(function(){
        var file = $(this).val();
        $(this).closest("li, p").find(".filename").attr("value",file);
      });
    }
	});
	
// ]]>
</script>
     
      <p class="fm-submit"><button type="submit">Save Changes</button></p>
      
    </form>

  </section>

</div>
</section>
<?php foot(); ?>
