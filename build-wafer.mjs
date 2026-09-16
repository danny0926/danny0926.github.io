import {build} from 'esbuild';
await build({entryPoints:['wafer-home.jsx'],bundle:true,minify:true,outfile:'wafer-home.js',define:{'process.env.NODE_ENV':'"production"'},legalComments:'eof'});
console.log('Built local wafer navigation.');
