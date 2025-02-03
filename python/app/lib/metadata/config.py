def gen_config_sql():
    """
    Generate comprehensive configuration metadata for various database tables.

    Returns:
        list: A list of dictionaries containing detailed table configurations.
    """
    return [
        {
            "table_name": "rest_area_place_facilities",
            "table_desc": (
                """
                    This table contains master rest area place facilities
                    id, data type: BIGINT, description of column: Unique identifier for each place type.\n
                    rest_area_place_id, data type: INT, description of column: Primary key that defines the type of place (e.g., restaurant, gas station, mosque).\n
                    name, data type: VARCHAR(255), description of column: The name of the place type (e.g., restaurant, gas station, mosque)\n
                    created_at, data type: DATETIME, description of column: Timestamp when the record was created.\n
                    updated_at, data type: TIMESTAMP, description of column: Timestamp when the record was last updated.\n
                """
            )
        },
        {
            "table_name": "rest_area_place_types",
            "table_desc": (
                """
                    This table defines the types of places (tenants) available in rest areas, such as restaurants, toilets, gas stations, and other facilities.\nColumns:\n
                    id, data type: BIGINT, description of column: Unique identifier for each place type.\n
                    name, data type: VARCHAR(255), description of column: The name of the place type (e.g., restaurant, toilet, e-toll, etc.).\n
                    code, data type: VARCHAR(255), description of column: A short code representing the place type.\n
                    created_at, data type: DATETIME, description of column: Timestamp when the record was created.\n
                    updated_at, data type: TIMESTAMP, description of column: Timestamp when the record was last updated.\n
                    is_active, data type: INT, description of column: Indicates whether this place type is active (1 = active, 0 = inactive).
                """
            )
        },
        {
            "table_name": "rest_area_places",
            "table_desc": (
                """
                    This table contains information about places (tenants) in rest areas, such as restaurants, gas stations, or mosques.\nColumns:\n
                    id, data type: BIGINT, description of column: Unique identifier for each place in a rest area.\n
                    image, data type: VARCHAR(255), description of column: URL or path to the image of the place.\n
                    name, data type: VARCHAR(255), description of column: The name of the place (e.g., KFC, Indomaret, Masjid, etc.).\n
                    rest_area_id, data type: VARCHAR(255), description of column: Foreign key linking to rest_areas.id to specify which rest area this place belongs to.\n
                    rest_area_place_type_id, data type: VARCHAR(255), description of column: Foreign key that defines the type of place (e.g., restaurant, gas station, mosque).\n
                    latitude, data type: VARCHAR(255), description of column: Geographical latitude of the place.\n
                    longitude, data type: VARCHAR(255), description of column: Geographical longitude of the place.\n
                    created_at, data type: DATETIME, description of column: Timestamp when the record was created.\n
                    updated_at, data type: TIMESTAMP, description of column: Timestamp when the record was last updated.\n
                    menu, data type: TEXT, description of column: Description of the menu or services offered by the place (if applicable).\n
                    menus, data type: TEXT, description of column: Additional menu details or options available at the place.
                """
            )
        },
        {
            "table_name": "rest_area_user",
            "table_desc": (
                """
                    This table links users with rest areas, potentially for tracking visits, favorites, or interactions.\nColumns:\n
                    id, data type: BIGINT, description of column: Unique identifier for each record.\n
                    rest_area_id, data type: BIGINT, description of column: Foreign key linking to rest_areas.id.\n
                    user_id, data type: BIGINT, description of column: Foreign key linking to the users table.\n
                    created_at, data type: TIMESTAMP, description of column: Timestamp when the record was created.\n
                    updated_at, data type: TIMESTAMP, description of column: Timestamp when the record was last updated.
                """
            )
        },
        {
            "table_name": "rest_areas",
            "table_desc": (
                """
                    This table contains master data of all rest areas along the highway.\nColumns:\n
                    id, data type: BIGINT, description of column: Unique identifier for each rest area.\n
                    image, data type: VARCHAR(255), description of column: URL or path to the image of the rest area.\n
                    name, data type: VARCHAR(255), description of column: The name of the rest area.\n
                    route, data type: CHAR(1), description of column: Indicates the highway direction; A = Away from KM 0 (outbound), B = Towards KM 0 (inbound).\n
                    latitude, data type: VARCHAR(255), description of column: Geographical latitude of the rest area.\n
                    longitude, data type: VARCHAR(255), description of column: Geographical longitude of the rest area.\n
                    highway_id, data type: INT, description of column: Foreign key linking to the specific highway where the rest area is located.\n
                    created_at, data type: TIMESTAMP, description of column: Timestamp when the record was created.\n
                    updated_at, data type: TIMESTAMP, description of column: Timestamp when the record was last updated.\n
                    id_realtime, data type: INT, description of column: ID reference for real-time status tracking (if applicable).\n
                    token, data type: VARCHAR(255), description of column: Authentication or access token for API usage related to this rest area.
                """
            )
        },
        {
            "table_name": "tbl_master_tarif",
            "table_desc": (
                """
                    This table contains toll tariff information for direct travel between toll gates.\nColumns:\n
                    id_ruas, data type: INT, description of column: Unique identifier for the toll segment.\n
                    nama_ruas, data type: VARCHAR(128), description of column: Name of the toll segment.\n
                    id_gerbang, data type: INT, description of column: Unique identifier for the toll gate.\n
                    nama_gerbang, data type: VARCHAR(128), description of column: Name of the toll gate.\n
                    tipe_gerbang, data type: VARCHAR(8), description of column: Type of toll gate (e.g., entry or exit).\n
                    id_asal_gerbang, data type: INT, description of column: Unique identifier for the starting toll gate.\n
                    nama_asal_gerbang, data type: VARCHAR(128), description of column: Name of the starting toll gate.\n
                    latitude_asal, data type: VARCHAR(255), description of column: Latitude coordinate of the starting toll gate.\n
                    longitude_asal, data type: VARCHAR(255), description of column: Longitude coordinate of the starting toll gate.\n
                    gol1, data type: INT, description of column: Toll tariff for vehicle class 1 (e.g., small cars).\n
                    gol2, data type: INT, description of column: Toll tariff for vehicle class 2 (e.g., medium trucks).\n
                    gol3, data type: INT, description of column: Toll tariff for vehicle class 3 (e.g., large trucks).\n
                    gol4, data type: INT, description of column: Toll tariff for vehicle class 4 (e.g., buses).\n
                    gol5, data type: INT, description of column: Toll tariff for vehicle class 5 (e.g., heavy trucks).\n
                    gol6, data type: INT, description of column: Toll tariff for vehicle class 6 (e.g., special vehicles).\n
                    created_at, data type: TIMESTAMP, description of column: Timestamp when the record was created.\n
                    updated_at, data type: TIMESTAMP, description of column: Timestamp when the record was last updated.\n
                    jenis_gerbang, data type: INT, description of column: Type of toll gate (entry, exit, or intermediate).\n
                    arah_tujuan, data type: INT, description of column: Direction of travel.\n
                    cluster, data type: INT, description of column: Cluster category for grouping toll segments.\n
                    aktif, data type: INT, description of column: Status of the toll segment (1 for active, 0 for inactive).
                """
            )
        },
        {
            "table_name": "tbl_tarif_tol",
            "table_desc": (
                """
                    This table contains toll tariff and route information for determining travel costs and paths.\nColumns:\n
                    id, data type: BIGINT, description of column: Unique identifier for each toll route record.\n
                    asal, data type: VARCHAR, description of column: The starting location of the toll journey.\n
                    latitude_asal, data type: VARCHAR, description of column: Latitude coordinate of the starting location.\n
                    longitude_asal, data type: VARCHAR, description of column: Longitude coordinate of the starting location.\n
                    tujuan, data type: VARCHAR, description of column: The destination location of the toll journey.\n
                    latitude_akhir, data type: VARCHAR, description of column: Latitude coordinate of the destination location.\n
                    longitude_akhir, data type: VARCHAR, description of column: Longitude coordinate of the destination location.\n
                    gol1, data type: INT, description of column: Toll tariff for vehicle class 1 (e.g., small cars).\n
                    gol2, data type: INT, description of column: Toll tariff for vehicle class 2 (e.g., medium trucks).\n
                    gol3, data type: INT, description of column: Toll tariff for vehicle class 3 (e.g., large trucks).\n
                    gol4, data type: INT, description of column: Toll tariff for vehicle class 4 (e.g., buses).\n
                    gol5, data type: INT, description of column: Toll tariff for vehicle class 5 (e.g., heavy trucks).\n
                    gol6, data type: INT, description of column: Toll tariff for vehicle class 6 (e.g., special vehicles).\n
                    keterangan, data type: VARCHAR, description of column: Additional information or notes regarding the route.\n
                    sistem, data type: INT, description of column: System type used in the toll calculation (e.g., open or closed system).\n
                    created_at, data type: DATETIME, description of column: Timestamp when the record was created.\n
                    updated_at, data type: DATETIME, description of column: Timestamp when the record was last updated.\n
                    regional, data type: VARCHAR, description of column: Regional classification of the toll route.\n
                    ruas_asal, data type: VARCHAR, description of column: Specific toll segment where the journey starts.\n
                    ruas_tujuan, data type: VARCHAR, description of column: Specific toll segment where the journey ends."
                """
            )
        },
        {
            "table_name": "highways",
            "table_desc": (
                """
                    This table contains information about highways, including their coordinates and status.\nColumns:\n
                    id, data type: BIGINT, description of column: Unique identifier for each highway.\n
                    name, data type: VARCHAR(255), description of column: The name of the highway.\n
                    start_latitude, data type: VARCHAR(255), description of column: Latitude coordinate where the highway starts.\n
                    start_longitude, data type: VARCHAR(255), description of column: Longitude coordinate where the highway starts.\n
                    end_latitude, data type: VARCHAR(255), description of column: Latitude coordinate where the highway ends.\n
                    end_longitude, data type: VARCHAR(255), description of column: Longitude coordinate where the highway ends.\n
                    created_at, data type: TIMESTAMP, description of column: Timestamp when the highway record was created.\n
                    updated_at, data type: TIMESTAMP, description of column: Timestamp when the highway record was last updated.\n
                    is_active, data type: INT, description of column: Status of the highway (1 = active, 0 = inactive).\n
                    created_by, data type: VARCHAR(25), description of column: User or system that created the record.\n
                    updated_by, data type: VARCHAR(25), description of column: User or system that last updated the record.\n
                    a, data type: VARCHAR(100), description of column: Placeholder column (needs clarification).\n
                    b, data type: VARCHAR(100), description of column: Placeholder column (needs clarification).
                """
            )
        }
    ]