const fs=require('fs'),{transform}=require('lightningcss');fs.writeFileSync('assets/styles.min.css',transform({filename:'styles.css',code:fs.readFileSync('assets/styles.css'),minify:true}).code);
