TODO : write an example of usage (MyGalery(options...))


The object can have:

    - thumbnail_path function, returning a path to the thumbnail to
    be displayed on the cell's background (used by cell_widget).

    - actions : tuple (libelle, function) used to create a context menu when clicked on
    the cell. A line will be created in the menu, with the text libelle, and function
    will be called when the line is clicked (used by cell_widget).