# Beyond Penn's Treaty Project V2

This project by the Haverford DS Team that will serve as the adjunct, and then final site for all digital research and transcription done on Beyond Penn's Treaty. It  provides access to linked and annotated versions of Quaker diaries, letters, and meeting records which record contact with American Indians, particularly the Seneca, beginning in the 1740s.This application makes it possible to search across our Quaker-related projects for people, organizations and places. 


The backend of this site uses FastAPI (documentation can be found at https://fastapi.tiangolo.com/).

Some frontend features use Bootstrap4. Documentation for Bootstrap can be found at https://getbootstrap.com/docs/4.1/getting-started/introduction/

Mansucripts in this project are mapped based on [TEI](http://www.tei-c.org/) rules to XML files. We then use Python and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to read and parse the XML files.

The features/visualizations on this site were made using the following libraries:

- [JQuery](http://jquery.com/)
- [DataTables](https://www.datatables.net/)
- [CartoLocation for Overviewmaps](https://carto.com/)



### For Developers:
#### run using:
`uvicorn main:app --reload`
#### Read　[Wiki](https://github.com/HCDigitalScholarship/QI/wiki)
#### If you want to make modifications on templates, [this page](https://github.com/HCDigitalScholarship/QI/wiki/Templates-Explanation) in Wiki should be helpful to give you some directions.
#### **For future developers of this project: Please read wiki for [existing issues](https://github.com/HCDigitalScholarship/QI/wiki/Issues-and-Suggested-to-do-list) of this project and explanations on existing features**



