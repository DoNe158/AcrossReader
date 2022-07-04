<h2>AcrossReader</h2>
<p>AcrossReader reads htm-files that are generated by the CAT tool Across for translating document. The code reads the htm file that can be exportet from Across
and converts it into a docx file displaying the translation in a table. Tags inside the source text and translation are removed or replaced. Every entry contains of
the segment id, the source text and the corresponding translation. 100% Fuzzy matches (duplicates) are removed, only the first occurrence is displayed and
stored in the docx file.</p>
<p>The purpose of this project is to transform translations made with the CAT tool Across into a docx file in a format-independent manner. Especially with XML files or HTML files, proofreading in this format is extremely confusing, which is why an extraction of the source text and translation should simplify this entire process. The attached example shows a translation of a text that is taken from a docx file.</p>
[example AcrossReader.pdf](https://github.com/DoNe158/AcrossReader/files/9041828/example.AcrossReader.pdf)
