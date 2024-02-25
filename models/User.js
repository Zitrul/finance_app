module.exports = (sequelize, DataTypes) => {
    const User = sequelize.define('User', {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true
        },
        username: {
            type: DataTypes.STRING,
            allowNull: false
        },
        password: {
            type: DataTypes.STRING,
            allowNull: false
        },
        first_name: {
            type: DataTypes.STRING,
            allowNull: true
        },
        last_name: {
            type: DataTypes.STRING,
            allowNull: true
        },
        telegram_auth: {
            type: DataTypes.STRING,
            allowNull: true
        },
        email_auth: {
            type: DataTypes.STRING,
            allowNull: false
        },
        telephone_number: {
            type: DataTypes.STRING,
            allowNull: true
        },
        telegram_bot_token: {
            type: DataTypes.STRING,
            allowNull: true
        },
        created_at: {
            type: DataTypes.NOW,
            allowNull: true
        }
    }, {
        freezeTableName: true,
        underscored: true
    });


    return User;
}