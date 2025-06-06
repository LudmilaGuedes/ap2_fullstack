class EscolaRouter:
    """
    Um router para direcionar operações do app 'escola' para o banco de dados 'config_escola'.
    """

    app_label_escola = 'administracao'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label_escola:
            return 'config_escola'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label_escola:
            return 'config_escola'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == self.app_label_escola or
            obj2._meta.app_label == self.app_label_escola
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.app_label_escola:
            return db == 'config_escola'
        return db == 'default'

class WebScrapingRouter:
    """
    Um router para direcionar operações do app 'webscraping' para o banco de dados 'config_scraping'.
    """

    app_label_scraping = 'webscraping'

    def db_for_read(self, model, **hints):
        """Direciona leituras para o banco 'config_scraping' se o modelo pertencer ao app webscraping."""
        if model._meta.app_label == self.app_label_scraping:
            return 'config_scraping'
        return None

    def db_for_write(self, model, **hints):
        """Direciona escritas para o banco 'config_scraping' se o modelo pertencer ao app webscraping."""
        if model._meta.app_label == self.app_label_scraping:
            return 'config_scraping'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Permite relações entre objetos do mesmo app 'webscraping'."""
        if (
            obj1._meta.app_label == self.app_label_scraping or
            obj2._meta.app_label == self.app_label_scraping
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Permite migrações apenas no banco correto."""
        if app_label == self.app_label_scraping:
            return db == 'config_scraping'
        return db == 'default'
