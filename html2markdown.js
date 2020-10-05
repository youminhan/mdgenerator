var TurndownService = require('turndown');
var fs = require('fs');
var turndownService = new TurndownService();


console.log(process.argv.slice(2)[0]);
var html_data = fs.readFileSync('temp/' + process.argv.slice(2)[0] + '.html', 'utf8');
var markdown_data = turndownService.turndown(html_data);

fs.writeFileSync('md/' + process.argv.slice(2)[0] + '.md', markdown_data);