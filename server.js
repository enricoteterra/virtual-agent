var http = require('http')
var url = require('url')
var fs = require('fs')
var path = require('path')
var baseDirectory = __dirname
var port = 9615

http.createServer(function (request, response) {
    try {
        var requestUrl = url.parse(request.url)

        var fsPath = baseDirectory+path.normalize(requestUrl.pathname)
        if ( requestUrl.pathname == "/")
            var fsPath = baseDirectory + '/index.html'

        var fileStream = fs.createReadStream(fsPath)
        console.log('serving: '+fsPath)

        fileStream.pipe(response)
        fileStream.on('open', function() {
             response.writeHead(200)
        })
        fileStream.on('error',function(e) {
             response.writeHead(404)     
             response.end()
        })
   } catch(e) {
        response.writeHead(500)
        response.end()     
        console.log(e.stack)
   }
}).listen(port)

console.log("listening on port "+port)