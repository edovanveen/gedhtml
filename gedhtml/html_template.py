def main(title, description, menu, header, content):
    return f"""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="description" content="{description}">
            <title>{title}</title>
            <link rel="stylesheet" href="pure-min.css">
            <link rel="stylesheet" href="style.css">
        </head>
        <body>

        <script src="chart.js"></script>
        <script src="chartjs-plugin-datalabels.js"></script>
        <script src="pedigree.js"></script>
        <script src="ui.js"></script>

        <div id="layout">

            <a href="#menu" id="menuLink" class="menu-link">
                <span></span>
            </a>

            <div id="menu">
                <div class="pure-menu">
                    <a class="pure-menu-heading" href="index.html">{title}</a>

                    {menu}
                </div>
            </div>

            <div id="main">
                <div class="header">
                    {header}
                </div>

                <div class="content">
                    {content}
                </div>
            </div>
        </div>

        </body>
        </html>

        """
    
def menu(start_page, name_index, about_page):
    return f"""
                    <ul class="pure-menu-list">
                        <li class="pure-menu-item"><a href="index.html" class="pure-menu-link">{start_page}</a></li>
                        <li class="pure-menu-item"><a href="name_index.html" class="pure-menu-link">{name_index}</a></li>
                        <li class="pure-menu-item"><a href="about.html" class="pure-menu-link">{about_page}</a></li>
                    </ul>
        """
