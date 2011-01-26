<?php include "./inc/template.php"; 
head(
  $title = 'Submit a New Demo | Mozilla Developer Network',
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
      <li><a href="demo-submit.php">Submit a New Demo</a></li>
    </ol>
  </nav>
</div>
</section>

<section id="content">
<div class="wrap">

  <section id="content-main" role="main">
    <h1 class="page-title">Submit a New Demo</h1>
    <p>Whether you are creating an amazing new way to experience the Web or just 
    experimenting with the latest technologies, we invite you to submit your own 
    demos to share with (or show off to) other web developers.</p>
    <p>Please complete the form below to ensure your demo is submitted to the 
    Demo Studio successfully.</p>

    <form id="demo-submit" class="submission" enctype="multipart/form-data" method="post" action="path/to/handler">
      <fieldset class="section">
        <legend><b>Describe Your Demo</b></legend>
        <p>Tell us more about your demo, including the name, description and the 
        technologies used. Please list the browsers you have tested it with.</p>
        
        <ul>
          <li>
            <label for="title">What is your demo's name?</label>
            <input type="text" id="title" name="title" />
          </li>
          <li>
            <label for="summary">Describe your demo in no more than two lines</label>
            <textarea id="summary" name="summary" rows="2" cols="60"></textarea>
          </li>
          <li>
            <label for="description">Describe your demo in more detail <em class="note">(optional)</em></label>
            <textarea id="description" name="description" rows="8" cols="60"></textarea>
          </li>
          <li>
            <fieldset class="inline">
              <legend><b>Select up to five technologies used in your demo.</b></legend>
              <ul id="tech-tags" class="cols-4">
                <li><label><input type="checkbox" name="audio"> Audio</label></li>
                <li><label><input type="checkbox" name="canvas"> Canvas</label></li>
                <li><label><input type="checkbox" name="css3"> CSS3</label></li>
                <li><label><input type="checkbox" name="device"> Device</label></li>
                <li><label><input type="checkbox" name="files"> Files</label></li>
                <li><label><input type="checkbox" name="fonts"> Fonts</label></li>
                <li><label><input type="checkbox" name="forms"> Forms</label></li>
                <li><label><input type="checkbox" name="geolocation"> Geolocation</label></li>
                <li><label><input type="checkbox" name="javascript"> JavaScript</label></li>
                <li><label><input type="checkbox" name="html5"> HTML5</label></li>
                <li><label><input type="checkbox" name="indexeddb"> IndexedDB</label></li>
                <li><label><input type="checkbox" name="dragndrop"> Drag and Drop</label></li>
                <li><label><input type="checkbox" name="mobile"> Mobile</label></li>
                <li><label><input type="checkbox" name="multitouch"> Multi-touch</label></li>
                <li><label><input type="checkbox" name="offline"> Offline Storage</label></li>
                <li><label><input type="checkbox" name="svg"> SVG</label></li>
                <li><label><input type="checkbox" name="video"> Video</label></li>
                <li><label><input type="checkbox" name="webgl"> WebGL</label></li>
                <li><label><input type="checkbox" name="websockets"> WebSockets</label></li>
                <li><label><input type="checkbox" name="webworkers"> Web Workers</label></li>
                <li><label><input type="checkbox" name="xhr"> XMLHttpRequest</label></li>
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
            <input type="text" id="video" name="video">
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
        <p>Upload a Zip file of your source code, in which the main page of your 
        demo is named <code>index.html</code> in the root directory.</p>
        
        <ul>
          <li>
            <label for="demo_package">Source code Zip file</label> 
            <input type="file" id="demo_package" name="demo_package" class="filebutton" title="Upload demo file&hellip;">
          </li>
          <li>
            <label for="source_code_url">Is your source code also available somewhere else on the web (e.g., github)? Please share the link.</label>
            <input type="text" id="source_code_url" name="source_code_url">
          </li>
          <li>
            <fieldset class="inline">
              <legend><b>Select all the licenses that apply to your source code.</b></legend>
              <ul>
                <li><label><input type="checkbox" id="lic-gpl" name="gpl"> GPL/LGPL</label></li>
                <li><label><input type="checkbox" id="lic-mpl" name="mpl"> MPL</label></li>
                <li><label><input type="checkbox" id="lic-apl" name="apl"> APL</label></li>
                <li><label><input type="checkbox" id="lic-bsd" name="bsd"> BSD/MIT</label></li>
                <li class="other"><label><input type="checkbox" id="lic-other" name="other"> Other</label>
                  <p class="other-value">
                    <label for="lic-other-url">Link to license text:</label>
                    <input type="text" id="lic-other-url" name="other-url">
                  </p>
                </li>
              </ul>
            </fieldset>
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
	
	$(document).ready(function(){
		$(".other .other-value").hide();
		$(".other input[type=checkbox]").click(function(){
		  if ( $(this).is(":checked") ) {
		    $(this).parents().find(".other-value").fadeIn(100);
		  }
		  else if ($(this).not(":checked")) {
		    $(this).parents().find(".other-value").fadeOut(100);
		    $(this).parents().find(".other-value input").attr("value",null);
		  }
		});
	});
// ]]>
</script>

      <fieldset class="section notitle">
        <ul>
          <li>
            <strong class="label">Show us you're human</strong>
            (recaptcha goes here)
          </li>
          <li class="check">
            <strong class="label"><label><input type="checkbox" name="agreement"> I accept</label> 
            the <a href="#">MDN Terms of Use</a> and <a href="#">Demo Studio Agreement</a></strong>
          </li>
        </ul>
      </fieldset>
      
      <p class="fm-submit"><button type="submit">Submit Demo</button></p>
      
    </form>

  </section>

</div>
</section>
<?php foot(); ?>
