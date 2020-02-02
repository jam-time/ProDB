import data_collection as dc
import static


def update_database_main(entity):
    session, response, site_group, site_record, page_count = dc.initialize_session(entity)

    if page_count is not None:
        for i in range(1, int(page_count)):
            page = i + 1



if __name__ == '__main__':
    for HOST in static.HOSTS:
        update_database_main(HOST)
