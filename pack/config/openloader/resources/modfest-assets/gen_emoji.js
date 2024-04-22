const font = {};
font.providers = [];
const style = {};
let char = 0xe000;

for await (const f of Deno.readDir('assets/modfest/textures/emoji')) {
	const value = String.fromCodePoint(char++);
	font.providers.push({
		type: 'bitmap',
		file: 'modfest:emoji/' + f.name,
		height: 9,
		ascent: 8,
		chars: [value],
	});

	style[f.name.substring(0, f.name.length - 4)] = value;
}

Deno.writeTextFileSync("assets/modfest/font/emoji.json", JSON.stringify(font))
Deno.writeTextFileSync("styled_chat_emoji.json", JSON.stringify(style))
