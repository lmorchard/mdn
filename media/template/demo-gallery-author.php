<?php include "./inc/template.php"; 
head(
  $title = 'Demos by Neil Gauldin | Demo Studio | Mozilla Developer Network',
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
      <li><a href="demo-gallery-author.php">Neil Gauldin</a></li>
    </ol>
  </nav>
  <p class="demo-submit"><a href="demo-submit.php" class="button">Submit a Demo</a></p>
</div>
</section>

<section id="content">
<div class="wrap">

  <header id="page-head" class="gallery">
    <div class="main author">
      <h1 class="page-title">
        <img src="./img/blank.gif" alt="" width="72" height="72" class="avatar"> Neil Gauldin 
        <!-- Only shown for the user and admins -->
        <a href="#" class="button edit">Edit Profile</a>
      </h1>
      <p class="loc">San Francisco, CA</p>
      <p class="web"><a href="#" rel="me external" class="url">http://www.itsneil.com</a></p>
    </div>
  </header>

  <section id="content-main" role="main">

    <div id="gallery-sort">
      <p class="count">7 Demos</p>
      <ul class="sort">
        <li><strong title="You are viewing these demos sorted by most views">Most Viewed</strong></li>
        <li><a href="#" title="Sort demos by most likes">Most Liked</a></li>
        <li><a href="#" title="Sort demos by most recently submitted">Most Recent</a></li>
      </ul>
    </div>

<script type="text/javascript" src="./js/jquery.hoverIntent.minified.js"></script>
<script type="text/javascript">
// <![CDATA[
	$(".gallery").ready(function(){
		$(".gallery").addClass("js");

    $(".gallery .demo").hoverIntent({
      interval: 250,
      over: function() {
        var content = $(this).html(),
            demo = $(this), 
            offs = $(this).offset();
        $("#content").prepend('<div class="demo demohover"><div class="in">'+content+'<\/div><\/div>');
        $("div.demohover").css({ left: offs.left, top: offs.top }).fadeIn(200).mouseleave(function() {
          $(this).fadeOut(200, function(){ 
            $(this).remove(); 
          });
        });
      }, 
      out: function() { /* do nothing */ }
    });

	});
// ]]>
</script>

<!-- NOTES:
     First item in each row needs the class "row-first". It's a strictly presentational class that only serves to 
     clear the floats of the row above, but it's necessary to preserve the layout.
-->
    <ul class="gallery">
      <li class="demo row-first">
        <h2 class="demo-title">
          <a href="demo-detail.php" title="See more about &ldquo;The Incredible Machine&rdquo; by Neil Gauldin">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> The Incredible Machine
          </a>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Neil Gauldin">Neil Gauldin</a></p>
        <div class="extra">
          <ul class="stats">
            <li class="views" title="This demo has been viewed 20,000 times">20,000</li>
            <li class="likes" title="3,000 people liked this demo">3,000</li>
            <li class="comments"><a href="demo-detail.php#comments" title="There are 100 comments for this demo">100</a></li>
          </ul>
          <p class="desc">Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
          <p class="launch"><a href="#" class="button" title="Launch &ldquo;The Incredible Machine&rdquo;">Launch</a></p>
        </div>
      </li>
      <li class="demo featured">
        <h2 class="demo-title">
          <a href="demo-detail.php" title="See more about &ldquo;Fantastic Voyage&rdquo; by Neil Gauldin">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> Fantastic Voyage
          </a>
          <strong class="flag">Featured</strong>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Neil Gauldin">Neil Gauldin</a></p>
        <div class="extra">
          <ul class="stats">
            <li class="views" title="This demo has been viewed 1,234 times">1,234</li>
            <li class="likes" title="151 people liked this demo">151</li>
            <li class="comments"><a href="demo-detail.php#comments" title="There are 3 comments for this demo">3</a></li>
          </ul>
          <p class="desc">Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
          <p class="launch"><a href="#" class="button" title="Launch &ldquo;Fantastic Voyage&rdquo;">Launch</a></p>
        </div>
      </li>
      <li class="demo">
        <h2 class="demo-title">
          <a href="demo-detail.php" title="See more about &ldquo;It's a Mad Mad Mad Mad Mad Mad World&rdquo; by Neil Gauldin">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> It&#8217;s a Mad Mad Mad Mad Mad Mad World
          </a>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Neil Gauldin">Neil Gauldin</a></p>
        <div class="extra">
          <ul class="stats">
            <li class="views" title="This demo hasn't been viewed by anyone yet">0</li>
            <li class="likes" title="Nobody has liked this demo yet">0</li>
            <li class="comments"><a href="demo-detail.php#comments" title="There are no comments yet for this demo">0</a></li>
          </ul>
          <p class="desc">Morbi in sem quis dui placerat ornare.</p>
          <p class="launch"><a href="#" class="button" title="Launch &ldquo;It's a Mad Mad Mad Mad Mad Mad World&rdquo;">Launch</a></p>
        </div>
      </li>

      <li class="demo featured row-first">
        <h2 class="demo-title">
          <a href="demo-detail.php" title="See more about &ldquo;Twenty Years to Midnight&rdquo; by Neil Gauldin">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> Twenty Years to Midnight
          </a>
          <strong class="flag">Featured</strong>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Neil Gauldin">Neil Gauldin</a></p>
        <div class="extra">
          <ul class="stats">
            <li class="views" title="This demo has been viewed 1,234 times">1,234</li>
            <li class="likes" title="151 people liked this demo">151</li>
            <li class="comments"><a href="demo-detail.php#comments" title="There are 3 comments for this demo">3</a></li>
          </ul>
          <p class="desc">Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
          <p class="launch"><a href="#" class="button" title="Launch &ldquo;Twenty Years to Midnight&rdquo;">Launch</a></p>
        </div>
      </li>
      <li class="demo">
        <h2 class="demo-title">
          <a href="demo-detail.php" title="See more about &ldquo;Bloodeye&rdquo; by Neil Gauldin">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> Bloodeye
          </a>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Neil Gauldin">Neil Gauldin</a></p>
        <div class="extra">
          <ul class="stats">
            <li class="views" title="This demo has been viewed 55 times">55</li>
            <li class="likes" title="7 people liked this demo">7</li>
            <li class="comments"><a href="demo-detail.php#comments" title="There are no comments yet for this demo">0</a></li>
          </ul>
          <p class="desc">Pellentesque fermentum dolor. Aliquam quam lectus, facilisis auctor, ultrices ut, elementum vulputate, nunc.</p>
          <p class="launch"><a href="#" class="button" title="Launch &ldquo;Bloodeye&rdquo;">Launch</a></p>
        </div>
      </li>
      <li class="demo">
        <h2 class="demo-title">
          <a href="demo-detail.php" title="See more about &ldquo;Modern Alchemy&rdquo; by Neil Gauldin">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> Modern Alchemy
          </a>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Neil Gauldin">Neil Gauldin</a></p>
        <div class="extra">
          <ul class="stats">
            <li class="views" title="This demo has been viewed 55 times">55</li>
            <li class="likes" title="7 people liked this demo">7</li>
            <li class="comments"><a href="demo-detail.php#comments" title="There are no comments yet for this demo">0</a></li>
          </ul>
          <p class="desc">Pellentesque fermentum dolor. Aliquam quam lectus, facilisis auctor, ultrices ut, elementum vulputate, nunc.</p>
          <p class="launch"><a href="#" class="button" title="Launch &ldquo;Modern Alchemy&rdquo;">Launch</a></p>
        </div>
      </li>

      <li class="demo row-first">
        <h2 class="demo-title">
          <a href="demo-detail.php" title="See more about &ldquo;Return to the House of Mummies, Part Two&rdquo; by Stephanie Acuba">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> Return to the House of Mummies, Part Two
          </a>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Neil Gauldin">Neil Gauldin</a></p>
        <div class="extra">
          <ul class="stats">
            <li class="views" title="This demo has been viewed 1,234 times">1,234</li>
            <li class="likes" title="151 people liked this demo">151</li>
            <li class="comments"><a href="demo-detail.php#comments" title="There are 3 comments for this demo">3</a></li>
          </ul>
          <p class="desc">Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
          <p class="launch"><a href="#" class="button" title="Launch &ldquo;Return to the House of Mummies, Part Two&rdquo;">Launch</a></p>
        </div>
      </li>
    </ul>
    
    <div id="gallery-foot">
      <p class="showing">1&ndash;7 of 7</p>
      <!-- no paging if there's only one page -->
      <p class="feed"><a href="#" rel="alternate" title="Subscribe to a feed of Neil Gauldin's demos">RSS</a></p>
    </div>

  </section><!-- /#content-main -->
  
  <aside id="content-sub" role="complementary">
    <form class="demo-search" method="post" action="/path/to/handler">
      <p>
        <input type="search" id="search-demos" placeholder="Search the Demo Studio" />
        <noscript><button type="submit">Search</button></noscript>
      </p>
    </form>
    
    <div class="module" id="demo-tags">
      <h3 class="mod-title">Browse by Technology</h3>
      <ul class="cols-2">
        <li><a href="demo-gallery.php">Audio</a></li>
        <li><a href="demo-gallery.php">Canvas</a></li>
        <li><a href="demo-gallery.php">CSS3</a></li>
        <li><a href="demo-gallery.php">Device</a></li>
        <li><a href="demo-gallery.php">Drag and Drop</a></li>
        <li><a href="demo-gallery.php">Files</a></li>
        <li><a href="demo-gallery.php">Fonts</a></li>
        <li><a href="demo-gallery.php">Forms</a></li>
        <li><a href="demo-gallery.php">Geolocation</a></li>
        <li><a href="demo-gallery.php">History</a></li>
        <li><a href="demo-gallery.php">HTML5</a></li>
        <li><a href="demo-gallery.php">IndexedDB</a></li>
        <li><a href="demo-gallery.php">JavaScript</a></li>
        <li><a href="demo-gallery.php">MathML</a></li>
        <li><a href="demo-gallery.php">Mobile</a></li>
        <li><a href="demo-gallery.php">Multi-touch</a></li>
        <li><a href="demo-gallery.php">Offline Storage</a></li>
        <li><a href="demo-gallery.php">SVG</a></li>
        <li><a href="demo-gallery.php">Video</a></li>
        <li><a href="demo-gallery.php">WebGL</a></li>
        <li><a href="demo-gallery.php">Websockets</a></li>
        <li><a href="demo-gallery.php">Web Workers</a></li>
        <li><a href="demo-gallery.php">XMLHttpRequest</a></li>
      </ul>
    </div> 
  </aside><!-- /#content-sub -->

</div>
</section>
<?php foot(); ?>
