
/*************************************************************************************************************************************************
*
* MSSQL
*
***************************************************************************************************************************************************/

/*
 * mssql - line_api_user_company
 */
CREATE TABLE line_api_user_company(
    no INT NOT NULL PRIMARY KEY IDENTITY(1,1),
    r_date DATE NULL,
    r_datetime DATETIME NULL,
    r_year VARCHAR(10) NULL,
    r_month VARCHAR(10) NULL,
    r_day VARCHAR(10) NULL,
    r_time VARCHAR(10) NULL,
    c_name VARCHAR(100) NULL,
    c_uid VARCHAR(100) NULL,
    c_company VARCHAR(100) NULL,
    c_c_pwd VARCHAR(50) NULL
);

/*
 * mssql - line_api_usage
 */
CREATE TABLE line_api_usage (
    no INT NOT NULL PRIMARY KEY IDENTITY(1,1),
    r_date DATE NULL,
    r_datetime DATETIME NULL,
    r_year VARCHAR(10) NULL,
    r_month VARCHAR(10) NULL,
    r_day VARCHAR(10) NULL,
    r_time VARCHAR(10) NULL,
    c_name VARCHAR(100) NULL,
    c_uid VARCHAR(100) NULL,
    c_company VARCHAR(100) NULL,
    c_p_msg VARCHAR(200) NULL,
);

/*
 * mssql - line_api_user
 */
CREATE TABLE line_api_user(
    no INT NOT NULL PRIMARY KEY IDENTITY(1,1),
    r_date DATE NULL,
    r_datetime DATETIME NULL,
    r_year VARCHAR(10) NULL,
    r_month VARCHAR(10) NULL,
    r_day VARCHAR(10) NULL,
    r_time VARCHAR(10) NULL,
    c_name VARCHAR(100) NULL,
    c_uid VARCHAR(100) NULL,
    c_company VARCHAR(100) NULL
);



/*************************************************************************************************************************************************
*
* MySQL
*
***************************************************************************************************************************************************/


/*
 * mysql - line_message_api
 */
create table line_message_api(
no int not null primary key AUTO_INCREMENT,
r_date date null,
r_datetime datetime null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
r_time varchar(10) null,
c_user varchar(100) null,
c_uid varchar(100) null,
c_kind varchar(30) null,
c_content varchar(40) null,
c_status varchar(10) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

