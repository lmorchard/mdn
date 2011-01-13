<?php include "./inc/template.php"; 
head(
  $title = 'The Incredible Machine | Mozilla Developer Network',
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
    </ol>
  </nav>
  
  <nav class="paging">
    <ul role="navigation">
      <li class="prev"><a href="#" title="Go to the previous demo, &ldquo;Demo Title&rdquo;">Prev</a></li>
      <li class="next"><a href="#" title="Go to the next demo, &ldquo;Demo Title&rdquo;">Next</a></li>
    </ul>
  </nav>
</div>
</section>

<section id="content">
<div class="wrap">

  <section id="content-main" role="main" class="full">
  
    <section id="demobox">
      <h1 class="page-title">The Incredible Machine</h1>
      <p class="byline">by <a href="#">Neil Gauldin</a> on <time datetime="">December 31, 2010</time></p>

      <!-- only shown to admins and the demo owner -->
      <p class="manage">
        <a href="#" class="button edit">Edit Demo</a> 
        <a href="#" class="button remove">Remove Demo</a>
      </p>

      <div class="demo-desc">
        <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
      </div>

      <ul class="tools">
        <li class="launch"><a href="#" class="button"><strong>Launch Demo</strong></a></li>
        <li class="like"><a href="#" title="Do you like this demo?">Like It</a></li>
        <!-- if they liked it already:
        <li class="unlike"><a href="#" title="You like this demo. Undo?">You Like</a></li>
        -->
        <li class="share"><a href="#share-opts" id="sharetoggle" title="Share this demo with your social network">Share It</a>
          <ul id="share-opts">
            <li class="sharetitle">Share It</li>
            <li class="twitter"><a href="#">Share on Twitter</a></li>
            <li class="facebook"><a href="#">Share on Facebook</a></li>
            <li class="link"><input id="shorturl" type="text" readonly="readonly" value="http://mzl.la/d44l20"></li>
          </ul>
        </li>
      </ul>
      
      <script type="text/javascript">
      $(document).ready(function(){
      	$("#share-opts").addClass("js").hide();
      	
      	$("#sharetoggle").click(function() {
          $("#share-opts").fadeIn(100);
          return false;
      	});
      	
        $("#share-opts").hover(
          function() {
            $(this).show();
          },
          function() {
            $(this).fadeOut(100);
            $("#sharetoggle").blur();
          }
        );
      	
        $(document).bind('click', function(e) {
          var $clicked = $(e.target);
          if (! $clicked.parents().hasClass("share"))
            $("#share-opts").hide();
        });
        
        $("a, input, textarea, button").bind('focus', function(e) {
          var $focused = $(e.target);
          if (! $focused.parents().hasClass("share"))
            $("#share-opts").hide();
        });
        
        $("#shorturl").focus(function() {
          $(this).select().addClass("focus");
        });
        $("#shorturl").click(function() {
          $(this).select().addClass("focus");
        });
        $("#shorturl").blur(function() {
          $(this).removeClass("focus");
        });
      
      });
      </script>

      <div class="demo-meta">
        <p class="tags">Built using <a href="#" rel="tag" title="See more demos made with lorem">lorem</a>, <a href="#" rel="tag" title="See more demos made with ipsum">ipsum</a>, <a href="#" rel="tag" title="See more demos made with dolor">dolor</a>, <a href="#" rel="tag" title="See more demos made with sit amet">sit amet</a></p>

        <ul class="stats">
          <li class="views">20,000 views</li>
          <li class="likes">3,000 likes</li>
          <li class="comments">100 comments</li>
        </ul>
      </div>
      
  		<div class="screenshots">
    		<ul class="nav-screens">
          <li class="nav-prev"><a href="#" class="prev" title="See the previous image">Previous</a></li>
      		<li class="nav-next"><a href="#" class="next" title="See the next image">Next</a></li>
        </ul>
  		  
    		<ul class="slider">
    		  <li class="panel">
    		    <img src="./img/fpo-slide1.jpg" alt="" width="480" height="360">
          </li>
          <li class="panel">
            <img src="./img/fpo-slide2.jpg" alt="" width="480" height="360">
          </li>
          <li class="panel">
            <img src="./img/fpo-slide4.jpg" alt="" width="480" height="360">
          </li>
        </ul>
  		</div><!-- /.screenshots -->

      <script type="text/javascript" src="./js/carousel.js"></script>
      
    </section><!-- /#demobox -->
    
    <section class="demo-more">

      <section class="moreabout">
        <h1>More About This Demo</h1>
        <p>Donec nec justo eget felis facilisis fermentum. Aliquam porttitor mauris sit amet orci. Aenean dignissim pellentesque felis.</p>
        <p>Morbi in sem quis dui placerat ornare. Pellentesque odio nisi, euismod in, pharetra a, ultricies in, diam. Sed arcu. Cras consequat.</p>
        <p>Praesent dapibus, neque id cursus faucibus, tortor neque egestas augue, eu vulputate magna eros eu erat. Aliquam erat volutpat. Nam dui mi, tincidunt quis, accumsan porttitor, facilisis luctus, metus.</p>
        <p>Phasellus ultrices nulla quis nibh. Quisque a lectus. Donec consectetuer ligula vulputate sem tristique cursus. Nam nulla quam, gravida non, commodo a, sodales sit amet, nisi.</p>
        <p>Pellentesque fermentum dolor. Aliquam quam lectus, facilisis auctor, ultrices ut, elementum vulputate, nunc.</p>
      </section>   
      
      <section id="comments">
        <header>
          <h1>5 comments so far</h1><!-- Should read "No comments yet" if there are no comments -->
          <!-- If logged in -->
          <p>Why not <a href="#comment-post">Add your own</a>?</p>
          <!-- If logged out:
          <p><a href="/register/">Register</a> or <a href="/login/">log in</a> to add your own.</p>
          -->
        </header>
        
        <ol id="comments-list" class="hfeed">
        	<li class="hentry" id="comment-123"><!-- every comment should have a unique ID for permalinking, however that ID is assigned (just sequential numbering I presume?) Remember that values of ID attributes in HTML cannot begin with a numeral -->
        	  <p class="entry-title vcard"><cite class="author fn"><a href="#" class="url" title="See Naomi Bellering's profile"><img class="photo" src="./img/blank.gif" alt="" width="48" height="48"> Naomi Bellering</a></cite> said,</p><!-- Avatar has empty alt -->
        		<p class="entry-meta">Posted <a href="#comment-123" rel="bookmark" title="Permanent link to this comment by Naomi Bellering"><time class="published" pubdate="pubdate" datetime="2010-12-31T18:48:02-08:00" title="2010-12-31">Dec 31, 2010</time></a></p>
        		<!-- NOTES: 
        		     See http://microformats.org/wiki/hatom for more on the hatom microformat. 
                 Published dates should be in the Y-m-d format in the title, following the microformat date pattern (less verbose than the datetime pattern but lesser impact on accessibility).
                 The datetime value can be the same as the title, or more verbose if we want to get really OCD about it: 'Y-m-d\TH:i:sP'
            -->
        		<blockquote class="entry-content">
        			<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec odio. Quisque volutpat mattis eros.</p>
        			<p>Nullam malesuada erat ut turpis. Suspendisse urna nibh, viverra non, semper suscipit, posuere a, pede.</p>
        		</blockquote>
        		
        		<ul class="comment-opts"><!-- only for logged-in users -->
        		  <li class="opt-reply"><a href="#comment-post" title="Reply to this comment by Naomi Bellering">Reply</a></li>
        		  <li class="opt-report"><a href="/report/confirm" title="Report this comment">Report</a></li><!-- Do you have to be logged in to report a comment? -->
        		  <li class="opt-delete"><a href="#" title="Edit this comment">Edit</a></li><!-- shown only to demo owner and admins... can users edit their own comments? -->
        		  <li class="opt-delete"><a href="/delete/confirm" title="Delete this comment">Delete</a></li><!-- shown only to demo owner and admins... can users delete their own comments? -->
        		</ul>
        	</li>
          
          <li class="hentry alt" id="comment-456">
        	  <p class="entry-title vcard"><cite class="author fn"><a href="#" class="url" title="See Byron Orpheus' profile"><img class="photo" src="./img/blank.gif" alt="" width="48" height="48"> Byron Orpheus</a></cite> said,</p>
        		<p class="entry-meta">Posted <a href="#comment-456" rel="bookmark" title="Permanent link to this comment by Byron Orpheus"><time class="published" datetime="" title="2011-01-05">5 days ago</time></a></p>
        		<blockquote class="entry-content">
        			<p>Phasellus ultrices nulla quis nibh. Quisque a lectus. Donec consectetuer ligula vulputate sem tristique cursus. Nam nulla quam, gravida non, commodo a, sodales sit amet, nisi.</p>
              <p>Pellentesque fermentum dolor. Aliquam quam lectus, facilisis auctor, ultrices ut, elementum vulputate, nunc.</p>
        		</blockquote>
        		<ul class="comment-opts"><!-- only for logged-in users -->
        		  <li class="opt-reply"><a href="#comment-post" title="Reply to this comment by Naomi Bellering">Reply</a></li>
        		  <li class="opt-report"><a href="/report/confirm" title="Report this comment">Report</a></li>
        		  <li class="opt-delete"><a href="#" title="Edit this comment">Edit</a></li>
        		  <li class="opt-delete"><a href="/delete/confirm" title="Delete this comment">Delete</a></li>
        		</ul>

        		<ol class="replies">
              <li class="hentry" id="comment-342">
                <!-- If the commenter's account has been deleted, the name shouldn't be linked (no profile to link to) and the avatar is replaced with the generic. The comment remains for posterity. -->
            	  <p class="entry-title vcard"><cite class="author fn"><img class="photo" src="./img/blank.gif" alt="" width="48" height="48"> Deleted Member</cite> said,</p>
            		<p class="entry-meta">Posted <a href="#comment-342" rel="bookmark" title="Permanent link to this comment"><time class="published" datetime="" title="2011-01-10">8 hours ago</time></a></p>
            		<blockquote class="entry-content">
            			<p>Suspendisse mauris. Fusce accumsan mollis eros. Pellentesque a diam sit amet mi ullamcorper vehicula. Integer adipiscing risus a sem. Nullam quis massa sit amet nibh viverra malesuada. Nunc sem lacus, accumsan quis, faucibus non, congue vel, arcu. Ut scelerisque hendrerit tellus. Integer sagittis. Vivamus a mauris eget arcu gravida tristique. Nunc iaculis mi in ante. Vivamus imperdiet nibh feugiat est.</p>
            		</blockquote>
            		<ul class="comment-opts">
            		  <li class="opt-reply"><a href="#comment-post" title="Reply to this comment by Naomi Bellering">Reply</a></li>
            		  <li class="opt-report"><a href="/report/confirm" title="Report this comment">Report</a></li>
            		  <li class="opt-delete"><a href="#" title="Edit this comment">Edit</a></li>
            		  <li class="opt-delete"><a href="/delete/confirm" title="Delete this comment">Delete</a></li>
            		</ul>

                <ol class="replies">
                  <li class="hentry alt" id="comment-985">
                	  <p class="entry-title vcard"><cite class="author fn"><a href="#" class="url" title="See Byron Orpheus' profile"><img class="photo" src="./img/blank.gif" alt="" width="48" height="48"> Byron Orpheus</a></cite> said,</p><!-- avatar has empty alt -->
                		<p class="entry-meta">Posted <a href="#comment-985" rel="bookmark" title="Permanent link to this comment by Byron Orpheus"><time class="published" datetime="" title="2011-01-10">25 minutes ago</time></a></p>
                		<blockquote class="entry-content">
                			<p>Sed adipiscing ornare risus. Morbi est est, blandit sit amet, sagittis vel, euismod vel, velit. Pellentesque egestas sem. Suspendisse commodo ullamcorper magna.</p>
                		</blockquote>
                		<ul class="comment-opts">
                		  <!-- No Reply option on deep-neested comments, depending on how many levels of replies we want to allow. -->
                		  <li class="opt-report"><a href="/report/confirm" title="Report this comment">Report</a></li>
                		  <li class="opt-delete"><a href="#" title="Edit this comment">Edit</a></li>
                		  <li class="opt-delete"><a href="/delete/confirm" title="Delete this comment">Delete</a></li>
                		</ul>
                	</li>
            		</ol>

            	</li>
        		</ol>

        	</li>
        </ol><!-- /#comment-list -->
        
        <!-- form only shown for logged-in users -->
        <form id="comment-post" method="post" action="/path/to/handler">
          <fieldset>
            <legend><span>Add your comment</span></legend>
            <div><textarea id="your-comment" name="comment" rows="6" cols="60"></textarea></div>
            <p><button type="submit">Comment</button></p>
          </fieldset>
        </form>

      </section>
    </section>
    
    <section id="demo-sub">
      
      <div class="module" id="source">
        <h3 class="mod-title">Get the Source Code</h3>
        <p class="download"><a href="#">Download the Source <span class="note">320 KB &middot; ZIP File</span></a></p>
        <p class="browse"><a href="#">Browse the Source <span class="note">Hosted on GitHub</span></a></p>
        <p class="license">This demo is released under the <a href="http://creativecommons.org/licenses/by-nc-nd/3.0/" rel="license">Creative Commons 3.0 By-NC-ND license</a>.</p>
      </div>
      
      <div class="module" id="moreby">
        <h3 class="mod-title">More by <a href="#">Neil Gaudlin</a></h3>
        <ul class="gallery">
          <li><a href="#"><img src="./img/fpo55.png" alt="" title="Demo Title" width="90" height="68"></a></li>
          <li><a href="#"><img src="./img/fpo55.png" alt="" title="Demo Title" width="90" height="68"></a></li>
        </ul>
      </div>
      
      <div id="demo-report">
        <h3>Report a Problem</h3>
        <ul>
          <li><a href="#">Demo is not working</a></li>
          <li><a href="#">Demo is inappropriate</a></li>
          <li><a href="#">Demo is not by this author</a></li>
        </ul>
      </div>
      
    </section>

  </section>

</div>
</section>
<?php foot(); ?>
