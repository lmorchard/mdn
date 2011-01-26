<?php include "./inc/template.php"; 
head(
  $title = 'Geolocation Demos | Demo Studio | Mozilla Developer Network',
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
      <li><a href="demo-gallery.php">Geolocation</a></li>
    </ol>
  </nav>
  <p class="demo-submit"><a href="demo-submit.php" class="button">Submit a Demo</a></p>
</div>
</section>

<section id="content">
<div class="wrap">

  <header id="page-head" class="gallery">
    <div class="main">
      <h1 class="page-title"><img src="./img/icons/geolocation.png" alt="" width="80" height="81"> Geolocation</h1>
      <p>The Geolocation API allows web applications to access the user's geographical location.</p>
    </div>
    
    <div class="learn">
      <h2>Learn More</h2>
      <ul>
        <li><a href="#">MDN Documentation</a></li>
        <li><a href="#">Wikipedia Article</a></li>
        <li><a href="#">W3C Spec</a></li>
      </ul>
    </div>
  </header>

  <section id="content-main" role="main">

    <div id="gallery-sort">
      <p class="count">100 Demos</p>
      <ul class="sort">
        <li><strong title="You are viewing up and coming demos">Up and Coming</strong></li>
        <li><a href="#" title="Sort demos by most views">Most Viewed</a></li>
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
      out: function() { /* do nothing */ },
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
          <a href="demo-detail.php" title="See more about &ldquo;Fantastic Voyage&rdquo; by Alejandra Divens">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> Fantastic Voyage
          </a>
          <strong class="flag">Featured</strong>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Alejandra Divens">Alejandra Divens</a></p>
        <div class="extra">
          <ul class="stats">
            <li class="views" title="This demo has been viewed 1,234 times">1,234</li>
            <li class="likes" title="151 people liked this demo">151</li>
            <li class="comments"><a href="demo-detail.php#comments" title="There are 100 comments for this demo">3</a></li>
          </ul>
          <p class="desc">Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
          <p class="launch"><a href="#" class="button" title="Launch &ldquo;Fantastic Voyage&rdquo;">Launch</a></p>
        </div>
      </li>
      <li class="demo">
        <h2 class="demo-title">
          <a href="demo-detail.php" title="See more about &ldquo;It's a Mad Mad Mad Mad Mad Mad World&rdquo; by Darryl McConnaughy">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> It&#8217;s a Mad Mad Mad Mad Mad Mad World
          </a>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Darryl McConnaughy">Darryl McConnaughy</a></p>
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

      <li class="demo row-first">
        <h2 class="demo-title">
          <a href="demo-detail.php" title="See more about &ldquo;Twenty Years to Midnight&rdquo; by Thaddeus Venture">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> Twenty Years to Midnight
          </a>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Thaddeus Venture">Thaddeus Venture</a></p>
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
          <a href="demo-detail.php" title="See more about &ldquo;Bloodeye&rdquo; by Jefferson Twilight">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> Bloodeye
          </a>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Jefferson Twilight">Jefferson Twilight</a></p>
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
          <a href="demo-detail.php" title="See more about &ldquo;&rdquo; by Amanda Parth">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> Modern Alchemy
          </a>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Amanda Parth">Amanda Parth</a></p>
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

      <li class="demo row-first">
        <h2 class="demo-title">
          <a href="demo-detail.php" title="See more about &ldquo;Careers in Science&rdquo; by Stephanie Acuba">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> Return to the House of Mummies, Part Two
          </a>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Stephanie Acuba">Stephanie Acuba</a></p>
        <div class="extra">
          <ul class="stats">
            <li class="views" title="This demo has been viewed 1,234 times">1,234</li>
            <li class="likes" title="151 people liked this demo">151</li>
            <li class="comments"><a href="demo-detail.php#comments" title="There are 3 comments for this demo">3</a></li>
          </ul>
          <p class="desc">Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
          <p class="launch"><a href="#" class="button" title="Launch &ldquo;Careers in Science&rdquo;">Launch</a></p>
        </div>
      </li>
      <li class="demo">
        <h2 class="demo-title">
          <a href="demo-detail.php" title="See more about &ldquo;A Tangled Skein&rdquo; by Byron Orpheus">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> A Tangled Skein
          </a>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Byron Orpheus">Byron Orpheus</a></p>
        <div class="extra">
          <ul class="stats">
            <li class="views" title="This demo has been viewed 1,234 times">1,234</li>
            <li class="likes" title="151 people liked this demo">151</li>
            <li class="comments"><a href="demo-detail.php#comments" title="There are 3 comments for this demo">3</a></li>
          </ul>
          <p class="desc">Sed adipiscing ornare risus. Morbi est est, blandit sit amet, sagittis vel, euismod vel, velit.</p>
          <p class="launch"><a href="#" class="button" title="Launch &ldquo;The Incredible Machine&rdquo;">Launch</a></p>
        </div>
      </li>
      <li class="demo featured">
        <h2 class="demo-title">
          <a href="demo-detail.php" title="See more about &ldquo;Pork Feathers&rdquo; by Benjamin Jonathan Jonah Jameson-Parker III, Esq.">
            <img src="./img/fpo55.png" alt="" width="200" height="150"> Pork Feathers
          </a>
          <strong class="flag">Featured</strong>
        </h2>
        <p class="byline vcard"><a href="demo-gallery-author.php" class="url fn" title="See more demos by Benjamin Jonathan Jonah Jameson-Parker III, Esq.">Benjamin Jonathan Jonah Jameson-Parker III, Esq.</a></p>
        <div class="extra">
          <ul class="stats">
            <li class="views" title="This demo has been viewed 21,092 times">21,092</li>
            <li class="likes" title="703 people liked this demo">703</li>
            <li class="comments"><a href="demo-detail.php#comments" title="There are 19 comments for this demo">19</a></li>
          </ul>
          <p class="desc">Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
          <p class="launch"><a href="#" class="button" title="Launch &ldquo;The Incredible Machine&rdquo;">Launch</a></p>
        </div>
      </li>
    </ul>
    
    <div id="gallery-foot">
      <p class="showing">27&ndash;36 of 100</p>
      <ul class="paging">
        <!-- No first or prev when we're on the first page, no next or last when we're on the last page -->
        <li class="first"><a href="#" title="Go to the first page">First</a></li>
        <li class="prev"><a href="#" title="Go to the previous page">Previous</a></li>
        <li class="next"><a href="#" title="Go to the next page">Next</a></li>
        <li class="last"><a href="#" title="Go to the last page">Last</a></li>
      </ul>
      <p class="feed"><a href="#" rel="alternate" title="Subscribe to a feed of Geolocation demos">RSS</a></p>
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
