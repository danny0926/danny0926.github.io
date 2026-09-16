import {build} from 'esbuild';
await build({entryPoints:['templates.jsx'],bundle:true,minify:true,outfile:'templates.js',define:{'process.env.NODE_ENV':'"production"'},legalComments:'eof'});
console.log('Built 10 local JSX design previews.');
