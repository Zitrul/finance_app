module.exports = (sequelize, DataTypes) => {
    const UserAssets = sequelize.define(
        "UserAssets",
        {
            id: {
                type: DataTypes.INTEGER,
                primaryKey: true,
                autoIncrement: true,
            },
            user_id: {
                type: DataTypes.INTEGER,
                allowNull: false,
            },
            company_name: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            asset_amount: {
                type: DataTypes.INTEGER,
                allowNull: false,
            },
            news_subscription: {
                type: DataTypes.BOOLEAN,
                allowNull: false,
            },
            stock_quote: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            created_at: {
                type: DataTypes.DATE,
                defaultValue: DataTypes.NOW,
                allowNull: true
            }
        },
        {
            freezeTableName: true,
            underscored: true,
        }
    );

    return UserAssets;
};
