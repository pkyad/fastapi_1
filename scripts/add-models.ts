/* eslint-disable no-console */
import checkbox, { Separator } from "@inquirer/checkbox";
import select from "@inquirer/select";
import fetch from "node-fetch";
import dbConfigs from "./../db.config.json";

const fs = require("fs");
const BASE_DIR = "app/db/models/";

const main = async (): Promise<void> => {
  const dbServiceSelected = await select({
    message: "Select a database namespace",
    choices: dbConfigs.databases.map((db) => {
      return { name: db.name, value: db };
    }),
  });

  const _allModelsResponse: any = await fetch(
    dbServiceSelected.schema_url + "/get-all-models"
  );

  const allModels = await _allModelsResponse.json();
  const choices: any[] = [];
  Object.keys(allModels).forEach((key) => {
    choices.push(new Separator());
    choices.push(new Separator(`${key}`));

    allModels[key].forEach((model: { name: string }) => {
      choices.push({
        value: model.name,
        name: `   ${model.name}`,
        checked: dbServiceSelected.models.includes(model.name as never),
      });
    });
  });

  const modelsSelected = await checkbox({
    message: "Select the SQL models you want to add to this project",
    choices,
    pageSize: 40,
    instructions: "Use tab to select / unselect the models",
  });

  const clonedDBConfig = JSON.parse(JSON.stringify(dbConfigs));

  clonedDBConfig.databases[0].models = modelsSelected as any;

  try {
    fs.writeFileSync(
      "db.config.json",
      JSON.stringify(clonedDBConfig),
      (err: any) => {
        console.error(err);
      }
    );
  } catch (err) {
    console.log(err);
  }

  const res = await fetch(
    dbServiceSelected.schema_url +
      "/py-sqlalchemy/?models=" +
      modelsSelected.join(",")
  );
  const jsonResponse = (await res.json()) as any[];

  if (!fs.existsSync(BASE_DIR)) {
    fs.mkdirSync(BASE_DIR);
  }

  jsonResponse.forEach((file) => {
    try {
      fs.writeFileSync(
        `${BASE_DIR}${file.file_name}`,
        file.file_content,
        (err: any) => {
          console.error(err);
        }
      );
    } catch (err) {
      console.log(err);
    }
  });
};

main().then(() => {
  console.log("Completed successfully");
});
