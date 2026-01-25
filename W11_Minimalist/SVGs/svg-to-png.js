const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

// --- CONFIGURATION ---
const TARGET_WIDTH = 7680;
const TARGET_HEIGHT = 4320;

// The "Magic Number": Render at 1/4th size, then upscale.
// Change to 1.0 if you want 100% vector precision (but it will be much slower).
const SCALE_FACTOR = 1; 

// --- BATCH PROCESSING ---
// 1. Read all files in the current directory
const files = fs.readdirSync('./');

// 2. Filter only SVG files
const svgFiles = files.filter(file => path.extname(file).toLowerCase() === '.svg');

if (svgFiles.length === 0) {
    console.log("❌ No SVG files found in this folder.");
    console.log("Make sure this script is in the same directory as your SVGs.");
    process.exit(1);
}

console.log(`✅ Found ${svgFiles.length} SVG files.`);
console.log(`⚙️  Target Resolution: ${TARGET_WIDTH}x${TARGET_HEIGHT}`);
console.log(`⚡ Using Hybrid Upscaling (x${SCALE_FACTOR} then up)`);
console.log("------------------------------------------------");

// 3. Process them sequentially (one by one to save memory)
(async () => {
    let processedCount = 0;

    for (const file of svgFiles) {
        try {
            const inputPath = file;
            
            // Create output filename: "image.svg" -> "image.png"
            // We use path.parse to get the name without extension
            const nameWithoutExt = path.parse(file).name;
            const outputPath = `${nameWithoutExt}.png`;

            console.log(`[${processedCount + 1}/${svgFiles.length}] Converting ${file} -> ${outputPath}...`);

            // The Hybrid Resize Pipeline
            await sharp(inputPath)
                // Step A: Render SVG small (Fast)
                .resize(Math.floor(TARGET_WIDTH * SCALE_FACTOR), Math.floor(TARGET_HEIGHT * SCALE_FACTOR), { 
                    kernel: 'lanczos3' 
                })
                // Step B: Upscale to Target Size (High Quality & Fast)
                .resize(TARGET_WIDTH, TARGET_HEIGHT, { 
                    kernel: sharp.kernel.lanczos3 
                })
                // Save
                .toFile(outputPath);

            console.log(`   ✅ Saved!`);
            processedCount++;

        } catch (err) {
            console.error(`   ❌ Error converting ${file}: ${err.message}`);
        }
    }

    console.log("------------------------------------------------");
    console.log("🚀 Batch Complete!");
})();