# Pandoc usage



1. Convert markdown to pdf

   ```
   pandoc Cosmos.md --latex-engine=xelatex -o example.pdf
   ```

   ​

2. Convert markdown to html


   ```
   pandoc -s MANUAL.md -o example2.html
   ```

   ​

3. Convert markdown to html using custom css

   ```
   pandoc --css=benjamin.css --to=html5 input.md -o output.html
   ```

   ​