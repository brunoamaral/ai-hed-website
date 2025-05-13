module.exports = {
	plugins: {
		"@fullhuman/postcss-purgecss": {
			content: ["./content/**/*.html", "./content/**/*.md", "/layouts/**/*.html"],
			safelist: {
				greedy: [
					"/.animate.*/",
					"/.text-align.*/",
					"/.clear-filter.*",
					"\\[filter-color\\=.*\\]", // Matches any [filter-color="..."]
					"/.row-.*",
				]
			},
			// fontFace: false,
			variables: false
		},
		autoprefixer: {},
		cssnano: {
			preset: [
				"default",
				{ "discardComments": { "removeAll": true } }
			]
		},
	}
};