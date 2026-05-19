---
icon: gear
---

# Supported Documents

This page lists the types of documents that are supported by the [document processing orchestrator](../tutorials/document-processing-orchestrator/).

## Document

1. DOCX
2. PDF
3. PPTX
4. XLSX
5. Google Docs (from URL)
6. Google Slides (from URL)
7. Google Spreadsheet (from URL)

## Plain Text

1. JSON
2. CSV
3. HTML
4. Java
5. JavaScript (JS)
6. JSX
7. Log files (.log)
8. Markdown
9. Python
10. TypeScript (TS)
11. TSX
12. Plain text files (.txt)

## URL

1. YouTube URLs - Will be ingested to text; may sometimes fail due to limitations from Google.

## Image

_These will be ingested as text._

1. HEIC
2. HEIF
3. JPEG (.jpg/.jpeg)
4. PNG
5. WEBP
6. TIFF

## Audio

_These will be ingested as text._

1. FLAC
2. MP3
3. OGG
4. WAV

## Video

_These will be ingested as text._

1. MP4
2. MPEG
3. MOV
4. AVI
5. MKV
6. WEBM
7. FLV
8. WMV
9. 3GP
10. OGV
11. ASF
12. MP2T
13. OGG

## Output

Document processing orchestrator can save into the following data stores:

1. Vector database
2. Tabular database
3. Knowledge Graph

## Limitations

These limitations are not planned to be supported:

1. PDF: Cannot extract advanced math equations.
2. DOCX: Cannot extract math equations.
3. YouTube URL:
   1. May sometimes fail due to limitations from Google.
4. Cannot process executable or package files (e.g. DMG, EXE, GZ, TAR, ZIP).
5. Cannot process files with proprietary exstensions (e.g. AI, PSD, DLL).
6. Cannot crawl or scrape URLs periodically.
   1. Projects are responsible to manage their own scheduler or cron-jobs.
