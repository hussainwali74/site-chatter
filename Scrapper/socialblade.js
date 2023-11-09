// Get individual elements within the main container
var socialblade_catogorized_url = [
  "https://socialblade.com/youtube/top/category/tech/mostsubscribed",
];

var d = [];
for (let i = 5; i < 105; i++) {
  var row = document.querySelector(
    "body > div:nth-child(12) > div:nth-child(2) > div:nth-child(" + i + ")"
  );
  var channel = {};

  // var rankDiv = mainContainer.querySelectorAll('div[style="float: left; width: 50px; color:#888;"]');
  var ranktext = row.children[0].textContent.trim();
  channel["rank"] = ranktext;

  var gradeDiv = row.children[1];
  var gradetext = gradeDiv.textContent.trim();
  channel["grade"] = gradetext;
  var channelnameDiv = row.children[2];
  var channelnametext = channelnameDiv.textContent.trim();
  channel["channelname"] = channelnametext;

  var link = channelnameDiv.querySelector("a");
  var linktext = link.getAttribute("href");
  if(linktext.includes('/youtube/c/')){
    linktext=linktext.replace('\/youtube\/c\/','https:\/\/www.youtube.com\/c\/')
}else{
      linktext=linktext.replace('\/youtube\/channel\/','https:\/\/www.youtube.com\/channel\/')

  }
  channel["link"] = linktext;

  var uploadsDiv = row.children[3];
  uploadstext = uploadsDiv.textContent.trim();
  var withoutCommas = uploadstext.replace(/,/g, ""); // Replace all commas with an empty string
  channel["uploads"] = withoutCommas;

  var subsdiv = row.children[4];
  var substext = subsdiv.textContent.trim();
  channel["substext"] = substext;

  var viewsDiv = row.children[5];
  var viewsText = viewsDiv.textContent.trim();
  channel["viewsText"] = viewsText;
  if (parseInt(channel["uploads"]) > 10) {
    d.push(channel);
  }
}
d;
